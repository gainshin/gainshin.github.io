#!/usr/bin/env python3
"""Tag keynote_speech_token_ledger.html with data-t and inject EN/ZH dictionaries.

Uses HTMLParser source offsets so opening tags are patched in place
(no BeautifulSoup reserialize; no rfind('>') on content).
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "assets/course/keynote_speech_token_ledger.html"
I18N = ROOT / "scripts/keynote_i18n"

CJK = re.compile(r"[\u4e00-\u9fff]")
SKIP = {"script", "style"}
BLOCK = {
    "p", "h1", "h2", "h3", "h4", "h5", "th", "td", "li", "dt", "dd",
    "figcaption", "blockquote", "summary", "label", "title",
}
BLOCK_CLASS = {
    "cover-label", "cover-title", "cover-subtitle", "tn-name", "sec-desc",
    "exec-lead", "tbl-label", "src-note", "es-kicker", "dt-label", "es-name",
    "es-desc", "rc-name", "rc-body", "rc-scale", "rc-go", "sl-title", "sl-lead",
    "sl-lane", "sl-bar", "title", "insight-label", "insight-body", "ws-name",
    "ws-body", "ws-en", "ws-io", "g-name", "g-stage", "item", "legend", "cap",
    "note", "kicker", "sub-title", "sub-desc", "num", "sc-cap", "sub-head",
    "es-legend", "sl-axis-label", "tk-honest", "th-label", "sc-label",
    "td-label", "td-body", "cover-meta", "sec-title", "tk-take", "tk-note",
    "takeaway-label", "strip-caption", "insight", "pill", "bd-ok", "bd-no",
    "tk-dual", "honest-q", "q-label", "step-name", "step-body", "cfg-label",
    "cfg-body", "arch-name", "arch-desc", "gantt-label", "act-name", "lg-name",
    "lg-desc", "layer-name", "item-name", "item-desc", "note-body", "callout",
    "callout-title", "drawer-title", "foot-note", "meta", "caption", "hint",
    "badge", "tag", "role", "ts-body", "ts-title", "ts-range", "ts-fail",
    "ts-name", "tt-key", "tt-val", "tier-name", "tier-desc", "pivot-tag",
    "config-marker", "config-tag", "sl-kicker", "mgmt-supp-label", "tt-title",
    "tt-label", "tt-body", "td-col",
}

CHROME_CSS = """
  /* ── Page chrome · back + tabs + lang ── */
  .nav-chrome {
    position: sticky;
    top: 0;
    z-index: 70;
    display: flex;
    align-items: stretch;
    gap: 8px;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0.55rem 0.75rem;
    background: var(--bg2);
    border-bottom: 1px solid var(--rule);
  }
  .nav-chrome .back-link {
    flex-shrink: 0;
    align-self: center;
    color: var(--ink);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.72rem;
    padding: 0.32rem 0.6rem;
    border: 1px solid var(--rule);
    background: #fff;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
  }
  .nav-chrome .back-link:hover { border-color: var(--red); color: var(--red); }
  .nav-chrome .lang-switch {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
    align-self: center;
  }
  .nav-chrome .lang-switch button {
    font: inherit;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    padding: 0.32rem 0.6rem;
    border: 1px solid var(--rule);
    background: #fff;
    color: var(--ink);
    border-radius: 4px;
    cursor: pointer;
    min-height: 0;
  }
  .nav-chrome .lang-switch button:hover { border-color: var(--red); color: var(--red); }
  .nav-chrome .lang-switch button.active { background: var(--ink); border-color: var(--ink); color: #fff; }
"""

SETLANG_JS = r"""
  /* KEYNOTE_I18N */
  var T = __T__;
  var SVGNS = "http://www.w3.org/2000/svg";
  var LANGTAG = {en: "en", zh: "zh-Hant"};
  var currentLang = "en";

  function setLang(lang) {
    currentLang = (lang === "zh") ? "zh" : "en";
    var dict = T[currentLang] || T.en;
    var nodes = document.querySelectorAll("[data-t]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute("data-t");
      var val = dict[key];
      if (val === undefined || val === null) continue;
      if (el.namespaceURI === SVGNS) {
        el.textContent = String(val).replace(/<[^>]+>/g, "");
      } else {
        el.innerHTML = val;
      }
    }
    var ariaNodes = document.querySelectorAll("[data-aria-t]");
    for (var a = 0; a < ariaNodes.length; a++) {
      var ak = ariaNodes[a].getAttribute("data-aria-t");
      var av = dict[ak];
      if (av !== undefined && av !== null) ariaNodes[a].setAttribute("aria-label", av);
    }
    document.documentElement.setAttribute("lang", LANGTAG[currentLang] || "en");
    try { localStorage.setItem("courseLang", currentLang); } catch (e) {}
    var btns = document.querySelectorAll(".lang-switch button");
    for (var j = 0; j < btns.length; j++) {
      btns[j].classList.toggle("active", btns[j].getAttribute("data-lang") === currentLang);
    }
  }

  document.querySelectorAll(".lang-switch").forEach(function (sw) {
    sw.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-lang]");
      if (b) setLang(b.getAttribute("data-lang"));
    });
  });

  (function initLang() {
    var initial = "en";
    try {
      var stored = localStorage.getItem("courseLang");
      if (stored === "zh" || stored === "en") initial = stored;
    } catch (e) {}
    setLang(initial);
  })();
"""


def linecol_to_offset(src: str):
    lines = src.splitlines(keepends=True)

    def off(line: int, col: int) -> int:
        return sum(len(l) for l in lines[: line - 1]) + col

    return off


class OffsetTree(HTMLParser):
    def __init__(self, src: str):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.to_off = linecol_to_offset(src)
        self.stack: list[dict] = []
        self.nodes: list[dict] = []

    def handle_starttag(self, tag, attrs):
        off = self.to_off(*self.getpos())
        gt = self.src.find(">", off)
        self.stack.append(
            {
                "tag": tag,
                "attrs": dict(attrs),
                "start": off,
                "open_end": gt,
                "own": [],
            }
        )

    def handle_startendtag(self, tag, attrs):
        return

    def handle_data(self, data):
        if self.stack:
            self.stack[-1]["own"].append(data)

    def handle_endtag(self, tag):
        while self.stack:
            n = self.stack.pop()
            end = self.to_off(*self.getpos())
            n["end"] = end
            n["inner"] = self.src[n["open_end"] + 1 : end]
            n["own_text"] = "".join(n["own"])
            self.nodes.append(n)
            if n["tag"] == tag:
                break


def is_chrome(n: dict) -> bool:
    if n["attrs"].get("data-lang"):
        return True
    cls = (n["attrs"].get("class") or "").split()
    if "lang-switch" in cls:
        return True
    if (n.get("inner") or "").strip() in ("繁中", "EN"):
        return True
    return False


def is_candidate(n: dict) -> bool:
    if n["tag"] in SKIP:
        return False
    if is_chrome(n):
        return False
    if n["attrs"].get("data-t"):
        return False
    cls = (n["attrs"].get("class") or "").split()
    if "tn-en" in cls or "cover-en" in cls:
        return False
    has = CJK.search(n.get("inner") or "") or CJK.search(n.get("own_text") or "")
    if not has:
        return False
    if n["tag"] in BLOCK or n["tag"] == "text":
        return True
    if any(c in BLOCK_CLASS for c in cls):
        return True
    return False


def outermost(cands: list[dict]) -> list[dict]:
    out = []
    for c in cands:
        contained = False
        for o in cands:
            if o is c:
                continue
            if o["start"] < c["start"] and o["end"] >= c["end"]:
                contained = True
                break
        if not contained:
            out.append(c)
    return out


def collect_targets(src: str) -> list[dict]:
    p = OffsetTree(src)
    p.feed(src)
    cands = [n for n in p.nodes if is_candidate(n)]
    outer = outermost(cands)
    outer_set_ranges = [(o["start"], o["end"]) for o in outer]
    leftover = []
    for n in p.nodes:
        if n["tag"] in SKIP:
            continue
        if is_chrome(n):
            continue
        if n["attrs"].get("data-t"):
            continue
        if not CJK.search(n.get("own_text") or ""):
            continue
        inside = any(s <= n["start"] and e >= n.get("end", n["start"]) for s, e in outer_set_ranges)
        if not inside:
            leftover.append(n)
            outer.append(n)
            outer_set_ranges.append((n["start"], n.get("end", n["start"])))
    outer.sort(key=lambda n: n["start"])
    return outer


def load_en_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    files = [
        I18N / "kn_long.en.json",
        I18N / "kn_short_0.en.json",
        I18N / "kn_short_1.en.json",
        I18N / "kn_short_2.en.json",
    ]
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        raise SystemExit("EN files missing:\n  " + "\n  ".join(missing))
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for item in data:
            zh = (item.get("zh") or "").strip()
            en = item.get("en")
            if zh and en is not None:
                mapping[zh] = en
    return mapping


def inject_chrome(src: str) -> str:
    if 'class="nav-chrome"' in src:
        return src

    src = src.replace('<html lang="zh-Hant">', '<html lang="en">', 1)

    old_title = "<title>講座講綱 — AI/UX 實務流 · H+M Token · 合成用戶用於POC · 知識蒸餾邊界</title>"
    new_title = '<title data-t="page.title">Keynote Outline — AI/UX Practice Flow · H+M Token · Synthetic Users for POC · Distillation Boundary</title>'
    if old_title not in src:
        raise SystemExit("title tag not found")
    src = src.replace(old_title, new_title, 1)

    # restyle .top-nav: drop sticky/max-width/padding/bg — those move to .nav-chrome
    old_top = """  .top-nav {
    position: sticky;
    top: 0;
    z-index: 70;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0.55rem 0.75rem;
    background: var(--bg2);
    border-bottom: 1px solid var(--rule);
    box-shadow: none;
  }"""
    new_top = CHROME_CSS + """
  .top-nav {
    flex: 1;
    min-width: 0;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 8px;
    max-width: none;
    margin: 0;
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
    position: static;
  }"""
    if old_top not in src:
        raise SystemExit("top-nav CSS block not found")
    src = src.replace(old_top, new_top, 1)

    src = src.replace(
        "    .top-nav { grid-template-columns: 1fr; max-width: none; }",
        """    .nav-chrome { flex-wrap: wrap; max-width: none; }
    .nav-chrome .back-link { order: 1; }
    .nav-chrome .lang-switch { order: 2; margin-left: auto; }
    .top-nav { order: 3; flex-basis: 100%; grid-template-columns: 1fr; max-width: none; }""",
        1,
    )
    src = src.replace("    .top-nav { display: none; }", "    .nav-chrome { display: none; }", 1)

    old_nav = """  <nav class="top-nav" role="tablist" aria-label="章節分頁 · 五段">"""
    new_nav = """  <div class="nav-chrome">
    <a class="back-link" href="../../course.html" data-t="nav.back">← Teaching Artifacts</a>
    <nav class="top-nav" role="tablist" aria-label="Section tabs · five parts" data-aria-t="nav.aria">"""
    if old_nav not in src:
        raise SystemExit("top-nav open tag not found")
    src = src.replace(old_nav, new_nav, 1)

    aria_swaps = [
        ('aria-label="前往 Token 帳本分頁"', 'aria-label="Go to the Token Ledger tab" data-aria-t="jump.token"'),
        ('aria-label="前往合成用戶 · POC 分頁"', 'aria-label="Go to the Synthetic User · POC tab" data-aria-t="jump.poc"'),
        ('aria-label="前往蒸餾邊界分頁"', 'aria-label="Go to the Distillation Boundary tab" data-aria-t="jump.boundary"'),
    ]
    for old, new in aria_swaps:
        if old not in src:
            raise SystemExit(f"aria-label not found: {old}")
        src = src.replace(old, new, 1)

    # close chrome after </nav> that follows the five tabs — the first </nav>
    close_at = src.find("</nav>")
    if close_at < 0:
        raise SystemExit("nav close not found")
    insert = """</nav>
    <span class="lang-switch">
      <button type="button" data-lang="en" class="active">EN</button>
      <button type="button" data-lang="zh">繁中</button>
    </span>
  </div>"""
    src = src[:close_at] + insert + src[close_at + len("</nav>") :]
    return src


def inject_js(src: str, t_json: str) -> str:
    js = SETLANG_JS.replace("__T__", t_json)
    if "/* KEYNOTE_I18N */" in src:
        start = src.find("  /* KEYNOTE_I18N */")
        end = src.find("    (function () {\n      var tabs")
        if start < 0 or end < 0 or end <= start:
            raise SystemExit("cannot replace existing i18n block")
        return src[:start] + js + "\n" + src[end:]
    marker = "    (function () {\n      var tabs"
    if marker not in src:
        raise SystemExit("tab IIFE not found")
    return src.replace(marker, js + "\n    (function () {\n      var tabs", 1)


def patch_data_t(src: str, targets: list[dict], key_of: dict[int, str]) -> str:
    """Insert data-t into opening tags, from the end so offsets stay valid."""
    pieces = []
    ordered = sorted(targets, key=lambda n: n["open_end"], reverse=True)
    html = src
    for n in ordered:
        key = key_of[id(n)]
        gt = n["open_end"]
        tag = html[n["start"] : gt + 1]
        if "data-t=" in tag:
            continue
        if tag.endswith("/>"):
            new_tag = tag[:-2] + f' data-t="{key}"/>'
        else:
            new_tag = tag[:-1] + f' data-t="{key}">'
        html = html[: n["start"]] + new_tag + html[gt + 1 :]
    return html


SPECIAL_EN = {
    "nav.back": "← Teaching Artifacts",
    "page.title": "Keynote Outline — AI/UX Practice Flow · H+M Token · Synthetic Users for POC · Distillation Boundary",
    "nav.aria": "Section tabs · five parts",
    "jump.token": "Go to the Token Ledger tab",
    "jump.poc": "Go to the Synthetic User · POC tab",
    "jump.boundary": "Go to the Distillation Boundary tab",
}
SPECIAL_ZH = {
    "nav.back": "← 返回教材清單",
    "page.title": "講座講綱 — AI/UX 實務流 · H+M Token · 合成用戶用於POC · 知識蒸餾邊界",
    "nav.aria": "章節分頁 · 五段",
    "jump.token": "前往 Token 帳本分頁",
    "jump.poc": "前往合成用戶 · POC 分頁",
    "jump.boundary": "前往蒸餾邊界分頁",
}


def main() -> None:
    src = HTML_PATH.read_text(encoding="utf-8")
    if 'class="nav-chrome"' not in src:
        src = inject_chrome(src)

    en_map = load_en_map()
    targets = collect_targets(src)

    T_en: dict[str, str] = dict(SPECIAL_EN)
    T_zh: dict[str, str] = dict(SPECIAL_ZH)
    key_of: dict[int, str] = {}
    zh_to_key: dict[str, str] = {}
    n = 1
    missing = []
    for t in targets:
        if t["attrs"].get("data-t") in SPECIAL_EN:
            continue
        zh = t["inner"].strip()
        if zh in zh_to_key:
            key = zh_to_key[zh]
        else:
            key = f"k{n:03d}"
            n += 1
            zh_to_key[zh] = key
            T_zh[key] = zh
            en = en_map.get(zh)
            if en is None:
                # try looser whitespace collapse
                collapsed = re.sub(r"\s+", " ", zh).strip()
                en = next((v for k, v in en_map.items() if re.sub(r"\s+", " ", k).strip() == collapsed), None)
            if en is None:
                missing.append(zh[:120])
                en = zh
            T_en[key] = en
        key_of[id(t)] = key

    if missing:
        miss_path = I18N / "missing_en.json"
        miss_path.write_text(json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"WARN {len(missing)} strings missing EN → fallback ZH (see {miss_path})")

    src = patch_data_t(src, targets, key_of)
    t_json = json.dumps({"en": T_en, "zh": T_zh}, ensure_ascii=False, separators=(",", ":"))
    src = inject_js(src, t_json)
    HTML_PATH.write_text(src, encoding="utf-8")
    print(f"wrote {HTML_PATH.name}: {len(T_en)} keys, {len(targets)} nodes tagged")


if __name__ == "__main__":
    main()
