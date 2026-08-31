#!/usr/bin/env python3
"""Inject data-t + EN/ZH dictionaries into teaching_brief_market_map.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "assets/course/teaching_brief_market_map.html"

# ── helpers ──────────────────────────────────────────────────────

def add_dt(html: str, content_start: str, key: str, nth: int = 0) -> str:
    start = 0
    seen = -1
    while True:
        found = html.find(content_start, start)
        if found < 0:
            raise SystemExit(f"NOT FOUND nth={nth} key={key}: {content_start[:80]!r}")
        gt = html.rfind(">", 0, found)
        lt = html.rfind("<", 0, gt + 1)
        tag = html[lt : gt + 1]
        if "data-t=" in tag:
            start = found + 1
            continue
        seen += 1
        if seen < nth:
            start = found + 1
            continue
        new_tag = tag[:-1] + f' data-t="{key}">'
        return html[:lt] + new_tag + html[gt + 1 :]


def sub_all(html: str, old: str, new: str) -> str:
    if old not in html:
        raise SystemExit(f"REPLACE MISS: {old[:80]!r}")
    return html.replace(old, new)


# ── EN dictionary (B2, no AI-pattern filler) ─────────────────────

EN = {
    "page.title": "AI/UX 5-Course Market Map · Course Comparison",
    "nav.back": "← Teaching Artifacts",
    "nav.brand": "AI/UX COURSE",
    "nav.t1": "Market Map",
    "nav.t2": "Paradigm Shift",
    "nav.t3": "Dataset",
    "nav.t4": "Dialectic",
    "nav.t5": "Harness × CoT",

    # repeats
    "cov.full": "Full match",
    "cov.partial": "Partial",
    "cov.thin": "Thin overlap",
    "cov.none": "Gap",
    "gap.closest": "Closest",
    "gap.gap": "Market gap",
    "pill.red": "Red ocean · winnable",
    "pill.blue": "Blue ocean",
    "t1.lesson1": "AI/UX paradigm shift",
    "t1.lesson5": "Leading designers through",
    "t1.s3_l1": "Paradigm shift",
    "t1.s3_l5": "Leading the team",
    "dt.ui": "UI shape",
    "dt.limit": "Hard constraints",
    "dt.prompt": "Must be in the prompt",
    "b.read": "READ",
    "b.write": "WRITE",
    "cfg.core": "Core roles",
    "cfg.orch": "Orchestrator",
    "cfg.wiki": "Wiki split",
    "cfg.harness": "Harness pressure",
    "cfg.fail": "Main failure mode",
    "cfg.ai": "Role of AI",
    "cfg.schema": "Wiki schema focus",
    "cfg.first": "First step",

    # tab 1 chrome
    "t1.title": '5-Course<span class="ornament">×</span>Market Map',
    "t1.intro": 'Map the five proposed AI/UX courses onto the May 2026 market. <strong>The first three already have decent competitors. Lessons 2, 4, and 5 are close to empty</strong> — especially "design knowledge as a queryable repository," "Red Team review + write-back," and "workflow governance for design leads." Current courses have not treated any of these as a system. Tables below split the view three ways: topic match, platform coverage, market gap.',
    "t1.s1_title": "5 courses × closest matches on Maven",
    "t1.s1_desc": 'One row per course, closest Maven competitors. Coverage uses a three-dot scale: <strong>●●●</strong> full topic match, <strong>●●○</strong> partial, <strong>●○○</strong> thin overlap, <strong>○○○</strong> empty.',
    "t1.th_lesson": "Lesson / topic",
    "t1.th_course": "Closest Maven course",
    "t1.th_instr": "Instructor / platform",
    "t1.th_cov": "Coverage",
    "t1.th_diff": "Key difference",
    "t1.leg1": '<span class="dot" style="color:var(--accent);">●●●</span> Full topic match',
    "t1.leg2": '<span class="dot" style="color:var(--accent-soft);">●●○</span> Partial',
    "t1.leg3": '<span class="dot" style="color:var(--ink-4);">●○○</span> Thin overlap',
    "t1.leg4": '<span class="dot" style="color:var(--ink-4);">○○○</span> Empty',

    "t1.r1d": "How strategy-layer UX changes with AI. Shape the product; do not just react.",
    "t1.r1k": "Leans toward “designing AI products,” not “the designer’s workflow changing.”",
    "t1.r2d": "Common AI interface failures, agentic UX, AI Design Canvas",
    "t1.r2k": "Pattern library. Does not ask what work is left for the designer.",
    "t1.r3d": "AI integration from a strategy seat. How AI workflows enter the product plan.",
    "t1.r3k": "Written for a PM / strategist, not for the designer’s own workflow.",
    "t1.r4d": "Stresses <strong>behavioral specification</strong>, <strong>system-level design</strong>, writing system prompts",
    "t1.r4k": "Cut is “define behavior for an AI product,” not “build a versioned knowledge repo for a design team.”",
    "t1.r5title": "— no direct match —",
    "t1.r5d": "“Design judgment → a markdown knowledge base you can query, cite, and version.” No course has made this a system yet.",
    "t1.r5k": "Strongest gap. Sits in the Karpathy LLM Wiki / Memex line.",
    "t1.r6d": "Cursor, Claude Code, Stitch, Lovable, Magic Patterns, Google AI Studio + a tool-choice frame",
    "t1.r6k": "Wide tool coverage. Stops at generation. Thin on the boundary between concept prototype and production-ready.",
    "t1.r7d": "Starts from Figma structure (components / variables / auto layout / naming) into an agentic workflow. Week 4 covers MCP + Code Connect + Claude Cowork",
    "t1.r7k": "Already live (not in development). Focus is Figma structure and agent handoff. No repo governance layer.",
    "t1.r8d": "4 weeks from idea to ready-to-ship product",
    "t1.r8k": "Build-first. Little structured data governance.",
    "t1.r9d": "Claude Code in a design workflow. CLAUDE.md / prompt library / phased build planning",
    "t1.r9k": "No Red Team review. No write-back into a knowledge base.",
    "t1.r10title": "— no full-loop match —",
    "t1.r10d": "Concept → Figma polish → freeze in repo → eng integration → <strong>Red Team review</strong> → <strong>write back to the wiki</strong>. That full turn is not taught anywhere.",
    "t1.r10k": "Strong gap. Competitors stop at “AI generated it → designer likes it → ship.”",
    "t1.r11d": "Rupa’s one-day workshop for leads. CLAUDE.md setup + workflow automation",
    "t1.r11k": "Aimed at a lead using tools personally, not at taking a design team through a workflow change.",
    "t1.r12d": "Maven UX-lead bundle: UX leadership, influence, design management (not AI-specific)",
    "t1.r12k": "Decoupled from AI workflow change. Pure UX leadership.",
    "t1.multi": "Multiple instructors",
    "t1.maven_list": "Maven · course list",
    "t1.r13title": "— almost no competitor —",
    "t1.r13d": "From tool adoption → <strong>knowledge governance + role split + workflow maturity</strong>. That design-leadership × AI/UX intersection has no dedicated course.",
    "t1.r13k": "Strongest gap. AI/UX classes lock onto individual skill. Leadership classes skip AI.",

    "t1.s2_title": "Other platforms × UX community",
    "t1.s2_desc": "UX schools, design platforms, and YouTube outside Maven. Against these five courses, most of this stays at tool how-tos or intro AI concepts. It does not carry the core framing.",
    "t1.th_plat": "Platform / instructor",
    "t1.th_content": "Course / content",
    "t1.th_rel": "Closest lessons",
    "t1.th_limit": "What it does / where it stops",
    "t1.p1c": "<strong>AI Design Engineering &amp; Vibe Coding</strong> (new cohort each month)<br>\n            Design-engineering workflow with Claude Code + Cursor + Figma MCP",
    "t1.p1rel": "Lessons 3 / 4",
    "t1.p1k": "Build-heavy. No Red Team, no write-back, no management layer.",
    "t1.p2c": "<strong>AI for UX Design</strong> (4 weeks)<br>\n            ChatGPT, Midjourney, Figma AI plugins folded into a UX process",
    "t1.p2rel": "Lessons 1 / 3",
    "t1.p2k": "Introductory. Thin on MCP / agentic workflow.",
    "t1.p3c": "<strong>Build Agentic AI Workflows for Product Design</strong><br>\n            Design workflow from prompts to systems",
    "t1.p3rel": "Lessons 3 / 4",
    "t1.p3k": "Topic is close. IxDF tone is best-practice roundup. Missing a live closed loop.",
    "t1.p4c": "<strong>AI in UX/UI Design</strong> (self-paced)<br>\n            AI for research / writing / prototype",
    "t1.p4rel": "Lesson 1",
    "t1.p4k": "Intro level. No MCP / agent / repo.",
    "t1.p5c": "<strong>AI-Powered UX Content Design Systems</strong><br>\n            Content agents and a rules system in Claude Code",
    "t1.p5rel": "Lesson 2",
    "t1.p5k": "Cut is a content design system. Neighbour to a full design-knowledge repo, different layer.",
    "t1.vallaure": "Christine Vallaure (further writing)",
    "t1.p6c": "UX Collective series <strong>\"Agentic AI, Design Systems &amp; Figma\"</strong><br>\n            Extra reading beyond the Maven course",
    "t1.p6rel": "Lesson 3",
    "t1.p6k": "Free extra. The Maven course (Build Scalable UI) is live — see Lesson 3.",
    "t1.p7c": "<strong>From Figma to Cursor with MCP</strong> (21 min)<br>\n            Figma MCP server + Cursor + Claude turning design into code",
    "t1.p7rel": "Lesson 3",
    "t1.p7k": "Pure tool tutorial. No theoretical frame.",
    "t1.maven_talks": "Maven free talks",
    "t1.p8c": "<strong>AI-Powered Design Workflows — Season 1</strong><br>\n            Designers from Perplexity, Flowglad, Henry on AI workflows",
    "t1.p8rel": "Lessons 1 / 3",
    "t1.p8k": "Free extra. Lots of cases, no systematic teaching.",

    "t1.s3_title": "Market gaps × where you pull ahead",
    "t1.s3_desc": "One line per course on the current market, plus the extra step your framing takes. First three are red ocean you can still win. Last two are close to empty.",
    "t1.th_l": "Lesson",
    "t1.th_state": "Current market",
    "t1.th_edge": "Your edge / higher-order cut",
    "t1.th_opp": "Opportunity",
    "t1.g1s": "Plenty of courses on “how to use AI” and “how to design AI products.”",
    "t1.g1e": "Cut is “<strong>what work is left for the designer as a role</strong>” — an existence question, not a tools question.",
    "t1.g2s": "The market has prompt libraries, design systems for AI, behavioral specs. Nobody has framed design knowledge as a versioned, queryable knowledge base.",
    "t1.g2e": "Treat <strong>design judgment</strong> as a markdown wiki agents can cite — Memex / Karpathy LLM Wiki, with a name of its own: <code>UX Dataset Repository</code>",
    "t1.g3s": "Tool tutorials overflow: Cursor, Lovable, v0, Figma MCP, Claude Code",
    "t1.g3e": "Cut is the boundary between <strong>concept prototype ↔ structured data ↔ production</strong>. Not tool operation.",
    "t1.g4s": "Existing courses stop the loop at “AI generated it → a human likes it → ship.” No review, no write-back.",
    "t1.g4e": "Full turn = concept → Figma polish → freeze in repo → eng integration → <strong>Red Team review</strong> → <strong>write back to the wiki</strong>. That loop is what makes the work auditable and repeatable.",
    "t1.g5s": "AI/UX classes lock onto individual skill. UX leadership classes skip AI. Nobody works the overlap.",
    "t1.g5e": "The claim is “<strong>one person can use it ≠ the team has it</strong>.” What a lead actually governs is <strong>knowledge + role split + workflow maturity</strong>.",
    "t1.verdict": 'If you get one sentence: <strong>“This is not how to use AI. It is how a design team turns AI into a governed workflow.”</strong> The gap across Lessons 2, 4, and 5 is where the value sits — <em>knowledge governance for design teams</em> has no occupant in Chinese or English. The first three lessons make people nod. The last two are what they pay for and forward to a colleague.',

    # tab 2
    "t2.title": 'Designers’ daily output<span class="ornament">×</span>AI structure layers',
    "t2.intro": 'Spread every UX activity in a typical six-sprint product project — <strong>28 document types, 8 phases</strong>. The point is not “designers are busy.” It answers Lesson 1: <em>If daily output is 28 document types, which ones can AI structure, and which must stay in Figma?</em> Result: <strong>86% is markdown-led structured knowledge</strong>. Only 14% is visual/spatial Figma-native. Lesson 2’s UX Dataset Repository governs that 86%.',
    "t2.tierA_name": "Pure Markdown · agent-native",
    "t2.tierA_desc": "Structured files with a schema. Agents can query, cite, and version them.<br>persona, use case, page list, tokens, decision log live here.",
    "t2.tierB_name": "Markdown-based HTML visualization",
    "t2.tierB_desc": "Prose body + embedded Mermaid / PlantUML / structured blocks.<br>journey map, IA, user flow, state diagram live here.",
    "t2.tierC_name": "Visual / spatial native",
    "t2.tierC_desc": "Figma is the delivery hub. Pencil can sit in the middle for polish. Local IDE still reads UX documentation.<br>wireframe, visual design, prototype, component live here.",
    "t2.gantt": "Full Gantt",
    "t2.insight": 'This <strong>86% of markdown that can be structured</strong> is the body of Lesson 1’s <em>finishing the spec</em>. Prompt-to-UI will not generate it, because it is <strong>not a screen</strong>. It is the in-between that makes a screen executable, auditable, and shippable to engineering. AI can draft, check consistency, and get cited in an agent workflow. The designer still judges — the artifact just extends from a Figma frame to versioned markdown.<br>\n            <br>\n            In short: <strong>Tier A + Tier B is everything the UX Dataset Repository governs</strong>. Tier C stays in Figma. Its metadata (component names, variants, token refs) still needs a wiki reference page, or agents cannot reason across tiers.',
    "t2.inv_title": "28 UX document types × storage rules",
    "t2.poc_title": "Turn PRD features into stack-specific variants with Gen-AI",
    "t2.poc_intro": 'Go back to the ochre band on the Gantt — <strong>S0 to S2</strong> — the <em>POC window</em>. Those three sprints are not “draw screens.” They turn a <strong>stack-agnostic</strong> PRD line ("users can manage notifications") into <strong>several variants you can compare inside a given stack</strong>. This section unpacks how to do that with AI tools without wasting the round.',
    "t2.sub31": "Same feature × four stacks",
    "t2.sub31d": 'Take <strong>notification settings</strong>: the PRD is one sentence; four stacks produce four design languages. The designer’s job is to <strong>put that stack’s constraints and idioms in the prompt</strong>. Skip it, and AI hands you web chrome + mobile gestures + an admin table taped together.',
    "t2.ts1": "Native app",
    "t2.ts1ui": "iOS / Android Settings child page; toggle list; grouped",
    "t2.ts1lim": "OS-level push permission, single narrow column, touch target ≥ 44pt",
    "t2.ts2": "Responsive web",
    "t2.ts2lim": "Multi-browser, no push (except Web Push), breakpoint behaviour",
    "t2.ts3": "SaaS admin",
    "t2.ts3lim": "role-based defaults, tenant isolation, audit log required",
    "t2.ts4": "Copilot · chat-first",
    "t2.ts4ui": "No settings page. Natural-language setup, smart defaults",
    "t2.ts4lim": "No persistent UI, finite context window, recall is unreliable",
    "t2.sub32": "AI Variants workflow",
    "t2.sub32d": 'Gen-AI is not valuable because it “gets it right once.” It is valuable because it <strong>gives you many at once</strong>. N variants are not a decision. You need a disciplined path that collapses them into one reviewable, traceable choice. Real judgment sits in <strong>Step 04</strong>. AI does not replace that.',
    "t2.ws1": "Extract the feature",
    "t2.ws1b": "Pull the smallest testable feature out of the PRD. Strip PM dressing.",
    "t2.ws1io": "<b>IN</b> · PRD paragraph<br>\n                <b>OUT</b> · feature statement",
    "t2.ws2": "Pin the stack",
    "t2.ws2b": "Tell the model which stack, primary viewport, and design-system tokens.",
    "t2.ws2io": "<b>IN</b> · feature + stack constraints<br>\n                <b>OUT</b> · full prompt context",
    "t2.ws3": "Fan out N variants",
    "t2.ws3b": "Ask for 3–5 variants on different UX bets: minimal / dense / progressive disclosure / smart default / opt-out.",
    "t2.ws3io": "<b>IN</b> · prompt<br>\n                <b>OUT</b> · N prototypes",
    "t2.ws4": "Judge against criteria",
    "t2.ws4b": "Not “which looks nice.” Score three: ① UX principles ② tech idioms ③ design-system consistency.",
    "t2.ws4io": "<b>IN</b> · N variants<br>\n                <b>OUT</b> · chosen variant + reasoning",
    "t2.ws5": "Log the decision",
    "t2.ws5b": "Write why B beat A into <code style=\"font-family:'IBM Plex Mono',monospace; font-size:10.5px; background:var(--hilite); padding:1px 4px;\">wiki/decisions/</code>. Keep rejected options, rejection reasons, and the trade-off.",
    "t2.ws5io": "<b>IN</b> · chosen variant<br>\n                <b>OUT</b> · immutable record",
    "t2.sub33": "Four recurring mistakes",
    "t2.sub33d": "POC failure is rarely the generation itself. It is <strong>what the designer does with the output</strong>. Four patterns show up every cohort.",
    "t2.th_pit": "Mistake",
    "t2.th_sym": "Symptom",
    "t2.th_fix": "Fix",
    "t2.pf1": "No stack specified",
    "t2.pf1s": "AI returns a chimera: web chrome + mobile gesture + admin table",
    "t2.pf1f": "First line of the prompt: <code>platform + primary viewport + design system</code>",
    "t2.pf2": "Every variant looks fine",
    "t2.pf2s": "Stuck in “generate one more round.” Nothing gets chosen.",
    "t2.pf2f": "Write <code>3 selection criteria</code> before you generate.",
    "t2.pf3": "Variants as deliverables",
    "t2.pf3s": "Drop an AI variant into Figma. Engineering finds logic holes and rebuilds.",
    "t2.pf3f": "Variants are material. Only <code>1 goes into Figma</code> for polish + spec finish.",
    "t2.pf4": "No written reason",
    "t2.pf4s": "Three weeks later the same decision restarts. A new hire asks “why?” and nobody can answer.",
    "t2.pf4f": "Step 5 is a hard gate. No <code>decision log</code>, no next feature.",
    "t2.poc_lab": "POC window<br>\n              in one line",
    "t2.poc_body": 'POC is “<strong>use AI to make comparable options; use designer judgment to close</strong>.” The ochre band spans S0–S2 because <strong>Tier A files</strong> (persona / use case / scenario) have to exist first, or Step 02 has nothing to constrain. <strong>Tier B files</strong> (journey, flow) need to form in parallel, or variants have no process to sit against.<br>\n              <br>\n              In short: <em>without Tier A + Tier B up front, AI Variants is a random generator.</em> POC is not “try a prototype.” It is the three-piece of <strong>structured prep + AI variants + designer judgment</strong>. Drop one piece and it collapses into the prompt-to-UI trick the market already sells.',

    # tab 3
    "t3.title": 'UX Dataset Repository<span class="ornament">×</span>curate and orchestrate',
    "t3.intro": 'C1 ended on: <em>“Tier A + Tier B is everything the UX Dataset Repository governs.”</em> C2 asks the next question — <strong>what does the repository look like? Where does it live? Who maintains it? How do agents read it?</strong> Answer: a private wiki co-maintained with an LLM. Markdown is the interface. The designer is <em>Orchestrator</em>. This chapter splits the architecture into five: pedigree, three-column layout, INGEST tool, curation, multi-agent orchestration.',
    "t3.s1_title": "Pedigree · Memex → LLM Wiki → UX Dataset Repository",
    "t3.s1_desc": 'What Vannevar Bush wanted in 1945, and what Andrej Karpathy restarted, is the same job — <em>“hand-maintained knowledge rots.”</em> Analog years could not solve it. The LLM era finally has a maintainer. Put UX Dataset Repository on that 75-year line and students hear it immediately: this is not AI hype. It is an engineering problem with a history.',
    "t3.ped1": "A private knowledge base that is <strong>actively curated</strong>. Bush’s core problem was links across documents — associative trails, cross-reference, backlinks. In analog years this stayed a sketch.",
    "t3.ped2": "Memex plus an LLM: <strong>humans curate sources, AI handles summarizing, cross-referencing, filing</strong>. A private, versioned markdown wiki. The model maintains it in the background. A human decides what matters.",
    "t3.ped2q": "Layers: raw sources · wiki pages · schema",
    "t3.ped3": "LLM Wiki specialised for <strong>product design</strong>: raw sources are PRD / journey / page-list; agents are Design / Research / Copy / Red Team; curator is the designer (a stacked identity).",
    "t3.ped3q": "Treat C1’s 86% Tier A+B files as knowledge agents can cite",
    "t3.s2_title": "Three columns · how AI/UX writing CoT orchestrates agents",
    "t3.s2_desc": 'Left column is <strong>immutable raw material</strong> (PRD, journey, module list…). Right column is <strong>specialist agents</strong> (Design / Research / Copy / Red Team). The wiki in the middle is the <strong>interface</strong>. The designer’s new identity (PM / UR / UI all count) is “<em>UX Writer / Curator</em>” — maintain the middle layer in CoT writing, and orchestrate the agents on the right.',
    "t3.svg_prd": "Product spec / feature list",
    "t3.svg_journey": "User journey",
    "t3.svg_mod": "Module list",
    "t3.svg_page": "Page list",
    "t3.svg_flow": "User flow",
    "t3.svg_cat": "Catalog",
    "t3.svg_log": "Chronological log",
    "t3.svg_pages": "Topic pages",
    "t3.svg_schema": "cross-ref conventions · filename rules · lint · voice &amp; tone",
    "t3.svg_schema2": "Changing schema beats editing every page",
    "t3.svg_ag1": "draw UI · ship prototype",
    "t3.svg_ag2": "interview · extract insight",
    "t3.svg_ag3": "UX microcopy · voice",
    "t3.svg_ag4": "contradiction · adversarial check",
    "t3.cap1": "<strong>Raw Sources</strong>\n            Raw material is immutable. Never rewrite it. Ingest once to markdown with <code>MarkItDown</code>.",
    "t3.cap2": "<strong>LLM Wiki</strong>\n            Three layers: catalog (<code>index.md</code>) · log (<code>log.md</code>) · curated pages · plus schema / CoT rules.",
    "t3.cap3": "<strong>UX Agents</strong>\n            Four specialist workers + one Orchestrator. Orchestrator is you — curate by writing CoT.",
    "t3.s3_title": "MarkItDown is the ticket, not the answer",
    "t3.s3_desc": 'The rust dashed INGEST line is the tool belt that turns raw sources (PRD, Word, PPT, PDF, meeting audio) into markdown. <strong>Microsoft MarkItDown</strong> (MIT, 87k stars, Python API + CLI + built-in MCP server) is the cheap reliable pick — and as Lesson 2 teaching material you have to name its <strong>boundary</strong> immediately: it only solves the cheap half.',
    "t3.md_does": 'MarkItDown <b>solves</b>',
    "t3.md_does_sub": "Format conversion · commodity infrastructure",
    "t3.md_d1": "Turn <code>.pdf</code> / <code>.docx</code> / <code>.pptx</code> / <code>.xlsx</code> into clean markdown",
    "t3.md_d2": "OCR + EXIF metadata on images",
    "t3.md_d3": "Speech transcription on audio (meeting recording → transcript)",
    "t3.md_d4": "One-shot ingest for HTML / CSV / JSON / XML / EPub / YouTube URL",
    "t3.md_d5": "Built-in <code>markitdown-mcp</code> server. Hang it on Claude Desktop / Claude Code",
    "t3.md_d6": "Plugin architecture. Write a custom converter (Figma export can go here later)",
    "t3.md_dont": 'MarkItDown <b>does not solve</b>',
    "t3.md_dont_sub": "Design-knowledge structure · the curator’s actual judgment",
    "t3.md_n1": "No <strong>summarize</strong> (the core move in Karpathy’s LLM Wiki)",
    "t3.md_n2": "No <strong>cross-reference</strong> (entity alignment across files)",
    "t3.md_n3": "No <strong>file / categorize</strong> (does this output belong in <code>persona/</code> or <code>decisions/</code>?)",
    "t3.md_n4": "Does not generate <code>index.md</code> / <code>log.md</code>",
    "t3.md_n5": "Does not know <strong>schema / frontmatter / naming convention</strong>",
    "t3.md_n6": "Does not know “design knowledge” — it cannot tell a page list from a user flow as objects",
    "t3.dist_h": "— Distortion risk: MarkItDown runs, design knowledge gets hollowed out",
    "t3.dist_d": '<strong>convert ≠ understand</strong>. Four source types get skipped in class — they <em>look</em> handled, and the design knowledge falls out in conversion. Students are not here to patch the tool. They are here to <strong>insert judgment where the tool distorts</strong>.',
    "t3.th_src": "Source type",
    "t3.th_after": "After MarkItDown",
    "t3.th_loss": "What design knowledge loses",
    "t3.th_patch": "What the curator must add",
    "t3.d1s": "Figma export PDF",
    "t3.d1a": "Images OCR’d or base64-embedded",
    "t3.d1l": "Component structure, tokens, variants all gone",
    "t3.d2s": "Flow diagram / wireframe",
    "t3.d2a": "Image turned into descriptive text (OCR)",
    "t3.d2l": "Spatial relations and edge meaning disappear",
    "t3.d2p": "Hand-write Mermaid, or restore link semantics in frontmatter",
    "t3.d3s": "Meeting audio",
    "t3.d3a": "Transcript (with timestamps)",
    "t3.d3l": "Who claimed what, who pushed back — needs hand markup",
    "t3.d4s": "Complex Word layout",
    "t3.d4a": "Main structure kept; comments / track changes often drop",
    "t3.d4l": "Side comments and track changes vanish",
    "t3.d4p": "Lift key comments to the page bottom by hand",
    "t3.s4_title": "From raw markdown to LLM Wiki: three curation jobs",
    "t3.s4_desc": "Turning MarkItDown’s raw markdown into an LLM Wiki agents can read is <strong>three jobs</strong> for the curator (the designer). That is Lesson 2’s core lab. MarkItDown is Lab 0 (self-study before class). These three are Lab 1 (in class).",
    "t3.c1n": "Add a frontmatter contract",
    "t3.c1b": "Define a YAML frontmatter schema per file type (persona, use case, decision, page): required fields, naming, tag vocabulary. Schema is the <strong>source of truth for structure</strong>.",
    "t3.c2n": "Build backlinks and tags",
    "t3.c2b": "<strong>A single markdown file is an island</strong> — finish a persona and you do not know which journeys it maps to; change a page and you do not know which decisions break. Write the links <strong>explicitly</strong> in frontmatter (<code>related:</code>) or <code>[[wiki-link]]</code> so agents can traverse.",
    "t3.c2e": "<b>IN</b> · one isolated markdown file<br>\n            <b>OUT</b> · a node on the cross-ref graph",
    "t3.c3n": "Register in index.md / log.md",
    "t3.c3b": "<code>index.md</code> is the catalog (agents navigate with it). <code>log.md</code> is the timeline (agents follow history). Every new file registers in both — the minimum discipline that <strong>stops the wiki rotting</strong>.",
    "t3.c3e": "<b>IN</b> · a new wiki page<br>\n            <b>OUT</b> · index.md + log.md updated together",
    "t3.ex_mark": "Example · WORKED EXAMPLE",
    "t3.ex_title": "How cross-ref lets an agent chain four files",
    "t3.ex_intro": '<strong>Scene:</strong> someone asks the agent “why is notification-prefs defaulting to digest?” Without cross-ref, the agent only sees the dead fact “default is digest.” It cannot answer <strong>why</strong>. With cross-ref, it walks the frontmatter trail across three files and returns a reason that sits on a persona.',
    "t3.jump1": "↓ follow <code>implements</code> to the matching decision",
    "t3.jump2": "↓ follow <code>applies_to_personas</code> to the persona",
    "t3.pre2": """---
type: decision
date: 2026-04-15
status: active
applies_to_personas: [sarah-busy-parent]
overrides: ios-default-immediate
trade_off: digest loses immediacy, buys retention
---""",
    "t3.pre3": """---
type: persona
id: sarah-busy-parent
pain: noise (99% of notifications do not matter)
behavior: once interrupted too often, she turns everything off
tolerance: digest is acceptable; immediate collapses her
---""",
    "t3.ans": "<strong>Agent answer:</strong> Core persona Sarah’s pain is noise — default immediate makes her kill all notifications, which is zero reach. Digest matches her tolerance and still delivers critical alerts. The recorded trade-off is “lose immediacy, buy retention.”",
    "t3.close": 'The path <strong>page → decision → persona</strong> is the “associative trail” <strong>Vannevar Bush</strong> wanted in <em>As We May Think</em> (1945) — paper and microfilm had no cheap way to maintain that graph (every card needed a hand index, and every change had to be chased forever). <em>The LLM era is the first time the maintainer is cheap.</em> That is what 4.2 cross-ref is actually doing.',
    "t3.s5_title": "Orchestrator = YOU · the designer’s stacked identity",
    "t3.s5_desc": 'Wiki is up. Agents have context they can cite. Agents will not decide <strong>who runs first, who feeds whom, when to merge, when to send it back</strong> — that is the Orchestrator, which is you. The day job (UI, research, copy) <em>stays</em>. Each role stacks <strong>UX Writer / Curator / Orchestrator</strong> on top.',
    "t3.ag1": "Draw UI, ship prototypes, operate Figma. C1’s POC variants run here.",
    "t3.ag2": "Interview transcription, insight extraction, persona patch suggestions.",
    "t3.ag3": "UX microcopy, tone &amp; voice consistency, locale alignment.",
    "t3.ag4": "Find contradictions, run adversarial checks, surface edge cases. Core of C4.",
    "t3.ag5": "Who runs first, who feeds whom, when to merge, when to send it back. Curate by writing CoT.",
    "t3.ag5r": "<b>READ</b> the whole wiki<br><b>WRITE</b> CoT · decisions · orchestration scripts",
    "t3.bridge": 'You now have a <strong>Wiki</strong>, <strong>Agents</strong>, and an <strong>Orchestrator</strong>. One problem is still open: <em>for an agent to actually “move Figma” — read the canvas, edit a component, write spec back to the repo — you need a <strong>protocol</strong>, not a prompt</em>.<br>\n          <br>\n          Next lesson (<strong>C3 · Figma × Gen-AI × MCP</strong>) is that loop: wiki → Figma → wiki. Figma opened a Dev Mode MCP server in 2025. That is the first time the loop has standard infrastructure.',

    # tab 4
    "t4.intro": "<strong>In planning</strong>: from concept prototype to a structured design flow.",

    # tab 6
    "t6.title": 'Hand the whole system<span class="ornament">×</span>to a team',
    "t6.intro": 'C1 gave you 86% structured judgment. C2 gave you wiki + agents + orchestrator. C3 gave you the dialectic loop. All of that still sits at <em>one person × one round</em>. <strong>C4 scales to team × ongoing operation</strong> — and that scale forces two things C1–C3 never touched: <strong>harness governance</strong> and <strong>multi-role setup</strong>. Then the course claim, named: <em>markdown + CoT writing is the shared interface</em>.',
    "t6.s1_title": "Net from C1–C3: personal scale → team scale",
    "t6.s1_desc": "Lay the three chapters flat: the system exists, but only at <strong>one person × one round</strong>. Put it on a 10-person team for 6 months and problems C1–C3 ignored show up. That is C4.",
    "t6.rc1n": "Paradigm shift",
    "t6.rc1b": "86% of UX files can be structured. POC variant discipline. Finishing the spec is the designer’s actual job.",
    "t6.rc1s": "One person · one feature",
    "t6.rc2b": "Three-column wiki + 4 agents + Orchestrator + three curation jobs (schema · cross-ref · categorize).",
    "t6.rc2s": "One person · one wiki",
    "t6.rc3b": "Thesis–antithesis–synthesis + mandatory Red Team + write-back. One dialectic = one feature closed.",
    "t6.rc3s": "One person · one round",
    "t6.rc4b": "Hand C1–C3 to a team — five-layer harness compression + two team configs + CoT as the shared interface.",
    "t6.rc4s": "Team · ongoing",
    "t6.s2_title": "Look back at the CoT interface graph: which nodes are still out",
    "t6.s2_desc": "Flatten the six node types from the V5 force-directed graph. C1–C3 already cover <strong>3 fully, 1 partly</strong>. <strong>2 are still out</strong>. The claim: <em>you cannot see those two while you are solo</em> — you hold every role, and one brain absorbs harness pressure. At team scale they have to be externalised.",
    "t6.inv1": '<code>CoT · markdown</code> has been in use the whole time, never named as a claim. <strong>Section 05 names it.</strong>',
    "t6.inv2": 'PM Designer / UR / UI / Visual / Orchestrator — C2 collapsed this to “Orchestrator = YOU.” <strong>Section 04 splits it.</strong>',
    "t6.inv3": "Design / Research / Copy / Red Team — fully covered in C2. Each agent has a read/write path wired to the wiki.",
    "t6.inv4": "Raw · Pages · Schema · index · log · cross-ref — covered by C2’s three columns + three curation jobs.",
    "t6.inv5": 'L1–L5 compression + Model View + Persistent View — C1–C3 never touched this. <strong>Section 03 fills it.</strong>',
    "t6.inv6": "Gen-AI · POC · tacit · Antigravity · Pencil · Red Team review — already collected across C1 (POC) and C3 (Dialectic).",
    "t6.s3_title": "Map five harness compression layers onto a design workflow",
    "t6.s3_desc": 'Harness started as an LLM-agent idea — manage the context window, compress, stop tokens exploding. C4’s map: <strong>treat that compression as a design team’s context-governance discipline</strong>. At team scale a sprint is stuffed with PRDs, design reviews, interview notes. That is design’s “token pressure.” Map the five layers onto sprint cadence and it becomes governance.',
    "t6.th_hop": "Harness op (LLM sense)",
    "t6.th_map": "Match in a design workflow",
    "t6.h1e": "Drop duplicate messages",
    "t6.h1m": "<strong>Merge duplicate specs / design-review notes for the same feature.</strong> Three people screenshot the same Figma frame in standup and write similar comments — collapse into one <code>decisions/d-2026-04-xxx.md</code>.",
    "t6.h2e": "Summarise tool output",
    "t6.h2m": "<strong>user research notes → persona / scenario page.</strong> UR agent runs 8 interviews and dumps a 200KB transcript. You cannot stuff that into the Design agent — excerpt into <code>personas/*.md</code> first. Keep verbatim quotes as evidence.",
    "t6.h3e": "Merge turns",
    "t6.h3m": "<strong>Merge several design crits in a sprint into one decision.</strong> “Default notification mode” got discussed three times, each with a tweak. Do not keep three progressive notes — merge into one <code>decision</code> and write the trade-off cleanly.",
    "t6.h4e": "Write a global summary",
    "t6.h4m": "<strong>sprint retro + next-sprint kickoff brief.</strong> Every 2 weeks: what decisions closed, what stayed open, what moves to the next backlog. Write it into <code>log.md</code>. That is how agents cite across sprints.",
    "t6.h5e": "Truncate oldest records",
    "t6.h5m": "<strong>Move old decisions to <code>archive/</code> (do not delete).</strong> A year-old decision still sitting in the active set gets eaten on every query — move it to <code>wiki/archive/2025-Q1/</code>. Search still reaches it via index; it does not crowd current context. Harness L5 on the agent side remembers “what was cut.” On the wiki side that is the archive index.",
    "t6.h6e": "What the model sees this turn",
    "t6.h6m": "<strong>This sprint’s working context</strong> — active personas, current-feature decisions, this sprint’s AC. When an agent runs a task, give it this slice. Do not dump the whole wiki.",
    "t6.h7e": "Full task history",
    "t6.h7m": "<strong>The whole wiki + archive</strong>. Agents pull fragments via query / index when needed. Nothing is preloaded into context. MV/PV split is the core of harness governance — and of design-team governance.",
    "t6.h_ins": 'Harness is not only for agent engineers — <strong>it is the context-governance discipline a design team has to learn at team scale</strong>. When the wiki has 1000 pages, 500 decisions, three years of history, agents stall without compression, new designers drown on day one, and even the Orchestrator cannot remember which file is which. <em>L1–L5 mapped onto sprint cadence is the engineering discipline that stops the wiki rotting.</em>',
    "t6.s4_title": "One PD (NA-style) · split team (Asia-style)",
    "t6.s4_desc": "A North American Product Designer often holds several jobs (research / IA / UI / interaction / microcopy in one head). Asian teams more often draw a hard line: PM Designer + UR + UI Designer + Visual + copy. <strong>Both setups are first-class AI Builders on this system</strong> — they just slice and govern differently.",
    "t6.cfgA": "Config A",
    "t6.cfgAh": "One Product Designer",
    "t6.cfgA_core": "One person holds <strong>research / IA / UI / interaction / microcopy</strong>",
    "t6.cfgA_orch": "You",
    "t6.cfgA_wiki": "Personal scratchpad + handoff docs for engineering. <code>personas/</code> and <code>decisions/</code> are mostly written for future-you",
    "t6.cfgA_h": "<strong>Low</strong> — one brain, one context, one voice",
    "t6.cfgA_f": "Judgment fatigue, scope creep, <em>all context in one head</em>, coming back from leave and not recognising last week’s decisions",
    "t6.cfgA_ai": "<strong>force multiplier</strong> — run every role’s work at ~5×",
    "t6.cfgA_s": "Personal voice + light frontmatter is enough. Weight sits on trade-offs in <code>decisions/</code>",
    "t6.cfgA_1": "<code>personal wiki</code> + Claude Code (standing in 1–2 weeks)",
    "t6.cfgB": "Config B",
    "t6.cfgBh": "Split team",
    "t6.cfgB_tag": "Asia-style · explicit role split",
    "t6.cfgB_core": "<strong>PM Designer + UR + UI Designer + Visual + copy</strong>, each a separate function",
    "t6.cfgB_orch": "Lead designer or design manager (not the PM)",
    "t6.cfgB_wiki": "Each role owns a slice — <code>UR own research/</code>, <code>UI own components/</code>, <code>PMD own decisions/</code>, <code>copy own copy/</code>. Shared schema, clear ownership",
    "t6.cfgB_h": "<strong>High</strong> — multiple agents at once, overlapping context, cross-role decision conflict",
    "t6.cfgB_f": "Knowledge islands, cross-role decision fights, <em>role-border wars</em> (who may edit the design system? who owns copy?)",
    "t6.cfgB_ai": "<strong>glue between role boundaries</strong> — fill the seams, check consistency across roles",
    "t6.cfgB_s": "strict schema + <code>owner</code> field + mandatory cross-role links + conflict protocol",
    "t6.cfgB_1": "Cross-role <strong>schema workshop</strong> (1 week) + shared <code>decision log</code> + Red Team agent",
    "t6.s4_claim": "<strong>The claim:</strong> both configs run on the same system (wiki + agents + harness). Difference is <em>how you slice</em> and <em>how dense the governance is</em> — which is the point of CoT as a shared interface (next section).",
    "t6.s5_title": "CoT as the shared interface · name the course claim",
    "t6.s5_desc": "This is the first time the course says the claim out loud: <strong>every node — different roles, agents, harness ops, team configs — shares one interface: markdown + CoT writing</strong>. That is why the two configs in Section 04 can run on one system. They trade work through this hub.",
    "t6.svg_foot": "— Remove CoT and the graph falls apart. Cohesion comes from this hub only.",
    "t6.hub": "<strong>Every node is pulled to the same centre: markdown · CoT writing.</strong> <em>Remove that interface and the graph falls apart.</em> This is the body of C1’s “finish the spec,” the substrate of C2’s wiki, the writing medium of C3’s three dialectic beats, and the language of C4’s harness governance.",
    "t6.axis_h": "— Why this hub matters: five compose axes",
    "t6.axis_d": "Other AI/UX workflow pitches bind to a tool or a platform (some design tool’s AI plugin). You get 5× speed and you cannot compose. Markdown + CoT is the only shared interface that <em>combines on five axes at once</em>:",
    "t6.cb1a": "i · across ROLES",
    "t6.cb1t": "Shared writing interface",
    "t6.cb1b": "UR / UI / Visual / copy all write markdown. No bespoke tool per role.",
    "t6.cb2a": "ii · across AGENTS",
    "t6.cb2t": "Shared context format",
    "t6.cb2b": "Design / Research / Copy / Red Team all eat markdown context. Agents can be chained.",
    "t6.cb3a": "iii · across TOOLS",
    "t6.cb3t": "Viewers are swappable",
    "t6.cb3b": "Obsidian / VS Code / Cursor / Claude Code / GitHub web all read markdown. Switching tools is cheap.",
    "t6.cb4a": "iv · across TEAMS",
    "t6.cb4t": "Config can evolve",
    "t6.cb4b": "Solo PD and split team share a substrate. Grow by splitting roles; shrink by collapsing them.",
    "t6.cb5a": "v · across TIME",
    "t6.cb5t": "Git is the history",
    "t6.cb5b": "Git records markdown changes. Five years later a new hire can still see why a decision landed that way.",
    "t6.s6_title": "Five maturity levels × entry path for two team configs",
    "t6.s6_desc": "Stretch the course deliverable into five maturity levels, with a staged path for each config. L0 is before class. L3 is C4’s main target. L4 is after the course.",
    "t6.m0n": 'Individual AI-tool user <span class="mat-name-tag">before class</span>',
    "t6.m0c": 'ChatGPT / Cursor speed up personal output. No wiki. <strong>Judgment lives in one head</strong>. AI is a “faster” tool, not a “compounding” tool.',
    "t6.m0i": "“I use ChatGPT.” “I ran a prototype in v0.”",
    "t6.m0p": "<b>Solo PD</b>\n            Stand up a personal wiki (1–2 sprints)\n            <b>Split Team</b>\n            cross-role schema workshop (1 week)",
    "t6.m1n": 'Personal wiki + a couple of agents <span class="mat-name-tag">end of C2</span>',
    "t6.m1c": "Structured markdown wiki. 1–2 agents on specific tasks. <strong>Judgment is externalised; a new hire can read what the last person was thinking</strong>.",
    "t6.m1i": "“Design decisions live in the wiki, not only in my head.”",
    "t6.m1p": "<b>Solo PD</b>\n            Add a Red Team agent (next 1–2 sprints)\n            <b>Split Team</b>\n            shared decision log + Red Team (1 sprint)",
    "t6.m2n": 'Dialectic-loop discipline <span class="mat-name-tag">end of C3</span>',
    "t6.m2c": "Every feature walks thesis–antithesis–synthesis. <strong>Red Team is a required node</strong>. The decision log is the audit trail.",
    "t6.m2i": "“If Red Team did not run, the feature is not done.”",
    "t6.m2p": "<b>Solo PD</b>\n            Harness compression to tidy the wiki (3–6 months)\n            <b>Split Team</b>\n            ownership borders + harness protocol (2–3 sprints)",
    "t6.m3n": 'Harness governance + multi-role governance <span class="mat-name-tag">C4 target</span>',
    "t6.m3c": "<strong>Five compression layers mapped to sprint cadence, one cross-role schema, a clear Model View / Persistent View border</strong>. Wiki does not rot. Agents still run. New hires are not flooded.",
    "t6.m3i": "“Every 2 weeks we write a global summary into log.md; old decisions go to archive on purpose.”",
    "t6.m3p": "<b>Solo PD</b>\n            Usually stops here (end of personal scale)\n            <b>Split Team</b>\n            one substrate across the design team (6–12 months)",
    "t6.m4n": 'Org-level CoT discipline <span class="mat-name-tag">after the course</span>',
    "t6.m4c": "<strong>The whole design org shares one substrate</strong>. Cross-team decision conflict has a path. Onboarding a new team is “point them at the wiki,” not “tell the story again.”",
    "t6.m4i": "“Week one of a new squad is forking the wiki schema.”",
    "t6.m4p": "<b>Solo PD</b>\n            Does not apply (you are still one person)\n            <b>Split Team</b>\n            org-level CoT council",
    "t6.finale": 'Four chapters. The argument graph is complete:<br>\n          <br>\n          <strong>C1</strong> is <em>why</em> — 86% of UX files can be structured. Specs do not finish themselves. Finishing the spec is the designer’s job.<br>\n          <strong>C2</strong> is <em>where</em> — three-column wiki + agents + orchestrator. Markdown is the substrate.<br>\n          <strong>C3</strong> is <em>how you run a round</em> — three dialectic beats, Red Team required, a feature is not done until the loop closes.<br>\n          <strong>C4</strong> is <em>how you scale</em> — harness governance on sprint cadence, two team configs on one substrate, CoT as the shared interface.<br>\n          <br>\n          One sentence to take back to work:<br>\n          <br>\n          <strong>Designers are not here to “learn AI.” They are here to write judgment as an interface, in CoT.</strong>\n          The interface is shared, so it composes with any agent, any role, any tool, any team scale. <em>That is the body of an AI/UX workflow.</em>',
}

ZH_OVERRIDE = {
    "page.title": "AI/UX 5 堂課市場對照表 · Course Comparison",
    "nav.back": "← 返回教材清單",
    "nav.brand": "AI/UX COURSE",
    "nav.t1": "Market Map",
    "nav.t2": "典範轉移",
    "nav.t3": "Dataset",
    "nav.t4": "Dialectic",
    "nav.t5": "Harness × CoT",
}

NOTE_EN = {
    "主要決策者、目標、KPI、否決權": "Key decision-makers, goals, KPIs, veto rights",
    "一段 narrative + 假設清單": "One narrative plus a hypothesis list",
    "結構化比較矩陣": "Structured comparison matrix",
    "逐字稿 + 標籤 + 引用 ID": "Transcript + tags + quote IDs",
    "高度結構化 frontmatter": "Highly structured frontmatter",
    "時序文字 + Mermaid 圖": "Sequential prose + Mermaid diagram",
    "Actor · Goal · Steps · 變體": "Actor · Goal · Steps · variants",
    "敘事 + 觸發條件 + 預期結果": "Narrative + trigger + expected outcome",
    "量化指標 + 來源 + 警戒值": "Metrics + source + alert thresholds",
    "tree-style markdown + Mermaid": "tree-style markdown + Mermaid",
    "ID · 模組名 · 範圍 · owner": "ID · module name · scope · owner",
    "頁面 ID · 模組 · 入口 · 狀態": "Page ID · module · entry · status",
    "步驟描述 + Mermaid sequence": "Step descriptions + Mermaid sequence",
    "主導覽 / 次導覽 / breadcrumb 規則": "Primary / secondary / breadcrumb rules",
    "Figma 原生；wiki 只放連結 + intent": "Figma-native; wiki holds link + intent only",
    "Figma 原生；tokens 對應在 wiki": "Figma-native; token mapping lives in wiki",
    "互動為主；wiki 描述互動意圖": "Interaction-first; wiki describes intent",
    "key-value · 多語版本 · tone 規則": "key-value · locale versions · tone rules",
    "markdown + Figma 標註 reference": "markdown + Figma annotation references",
    "情境 × 狀態 二維表": "Scenario × state matrix",
    "Given / When / Then 結構": "Given / When / Then structure",
    "markdown + Mermaid stateDiagram": "markdown + Mermaid stateDiagram",
    "對象 · 任務 · 量測 · 出場條件": "Audience · tasks · measures · exit criteria",
    "逐條發現 + 證據 + 建議": "Finding + evidence + recommendation, one per item",
    "WCAG 條目對照 + 例外": "WCAG mapping + exceptions",
    "markdown 敘述 + JSON source": "markdown narrative + JSON source",
    "Figma 主，wiki metadata 對應": "Figma is source; wiki holds metadata",
    "時序記錄；每條 immutable": "Chronological log; each entry immutable",
}

SETLANG_JS = r'''
  var T = __T_JSON__;
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
    document.documentElement.setAttribute("lang", LANGTAG[currentLang] || "en");
    try { localStorage.setItem("courseLang", currentLang); } catch(e) {}
    var btns = document.querySelectorAll(".lang-switch button");
    for (var j = 0; j < btns.length; j++) {
      btns[j].classList.toggle("active", btns[j].getAttribute("data-lang") === currentLang);
    }
    if (tab2Initialized) rerenderTab2();
  }

  function rerenderTab2() {
    var svg = document.getElementById("gantt-svg");
    if (svg) while (svg.firstChild) svg.removeChild(svg.firstChild);
    var table = document.getElementById("detail-table");
    if (table) table.innerHTML = "";
    renderGantt();
    renderDetailTable();
  }

  document.querySelectorAll(".lang-switch").forEach(function(sw) {
    sw.addEventListener("click", function(e) {
      var b = e.target.closest("button[data-lang]");
      if (b) setLang(b.getAttribute("data-lang"));
    });
  });
'''


def patch_gantt(html: str) -> str:
    html = html.replace(
        "note: '主要決策者、目標、KPI、否決權' }",
        "note: '主要決策者、目標、KPI、否決權', note_en: 'Key decision-makers, goals, KPIs, veto rights' }",
    )
    for zh, en in NOTE_EN.items():
        old = f"note: '{zh}' }}"
        new = f"note: '{zh}', note_en: '{en}' }}"
        if old in html:
            html = html.replace(old, new, 1)
        else:
            old2 = f'note: "{zh}" }}'
            new2 = f'note: "{zh}", note_en: "{en}" }}'
            if old2 in html:
                html = html.replace(old2, new2, 1)
            elif zh not in ("主要決策者、目標、KPI、否決權",):
                # already patched first one; others must exist
                if f"note_en: '{en}'" not in html and f'note: \'{zh}\'' in html:
                    raise SystemExit(f"note not patched: {zh}")
    # first item already handled; verify all notes have note_en
    missing = []
    for zh, en in NOTE_EN.items():
        if f"note_en: '{en}'" not in html and f'note_en: "{en}"' not in html:
            missing.append(zh)
    if missing:
        raise SystemExit("note_en missing: " + " | ".join(missing))

    html = html.replace(
        "    }, s.zh);",
        "    }, currentLang === 'zh' ? s.zh : s.en);",
        1,
    )
    html = html.replace(
        "  }, '— POC 階段 —');",
        "  }, currentLang === 'zh' ? '— POC 階段 —' : '— POC PHASE —');",
        1,
    )
    html = html.replace(
        """    }, phase.zh));

    phaseG.appendChild(el('text', {
      x: 15 + (phase.zh.length * 16), y: yCursor + 20,""",
        """    }, currentLang === 'zh' ? phase.zh : phase.en));

    phaseG.appendChild(el('text', {
      x: 15 + ((currentLang === 'zh' ? phase.zh : phase.en).length * (currentLang === 'zh' ? 16 : 8.5)), y: yCursor + 20,""",
        1,
    )
    html = html.replace(
        "      }, act.zh));",
        "      }, currentLang === 'zh' ? act.zh : act.en));",
        1,
    )
    html = html.replace(
        """      actG.appendChild(el('text', {
        x: 150, y: rowY + 14,
        'font-family': 'IBM Plex Mono, monospace',
        'font-size': 8.5,
        'letter-spacing': '0.1em',
        fill: '#a89e87',
      }, act.en));""",
        """      if (currentLang === 'zh') {
        actG.appendChild(el('text', {
          x: 150, y: rowY + 14,
          'font-family': 'IBM Plex Mono, monospace',
          'font-size': 8.5,
          'letter-spacing': '0.1em',
          fill: '#a89e87',
        }, act.en));
      }""",
        1,
    )
    html = html.replace(
        """  thead.innerHTML = `
    <tr>
      <th style="width:90px;">Tier</th>
      <th style="width:240px;">文件</th>
      <th style="width:110px;">主要 Sprint</th>
      <th style="width:280px;">儲存位置 / 格式</th>
      <th>說明</th>
    </tr>
  `;""",
        """  thead.innerHTML = currentLang === 'zh' ? `
    <tr>
      <th style="width:90px;">Tier</th>
      <th style="width:240px;">文件</th>
      <th style="width:110px;">主要 Sprint</th>
      <th style="width:280px;">儲存位置 / 格式</th>
      <th>說明</th>
    </tr>
  ` : `
    <tr>
      <th style="width:90px;">Tier</th>
      <th style="width:240px;">Document</th>
      <th style="width:110px;">Main sprint</th>
      <th style="width:280px;">Storage / format</th>
      <th>Notes</th>
    </tr>
  `;""",
        1,
    )
    html = html.replace(
        "      ? '持續 · ongoing'",
        "      ? (currentLang === 'zh' ? '持續 · ongoing' : 'ongoing')",
        1,
    )
    html = html.replace(
        """        <div class="doc-name">${doc.zh} <span style="color:var(--ink-3); font-weight:400;">/ ${doc.phaseZh}</span></div>
        <div class="doc-en">${doc.en}</div>""",
        """        <div class="doc-name">${currentLang === 'zh' ? doc.zh : doc.en} <span style="color:var(--ink-3); font-weight:400;">/ ${currentLang === 'zh' ? doc.phaseZh : doc.phaseEn}</span></div>
        <div class="doc-en">${currentLang === 'zh' ? doc.en : doc.zh}</div>""",
        1,
    )
    html = html.replace(
        "      <td>${doc.note}</td>",
        "      <td>${currentLang === 'zh' ? doc.note : (doc.note_en || doc.note)}</td>",
        1,
    )
    html = html.replace(
        "      allDocs.push({ ...act, phaseOrder: pIdx, phaseZh: phase.zh });",
        "      allDocs.push({ ...act, phaseOrder: pIdx, phaseZh: phase.zh, phaseEn: phase.en });",
        1,
    )
    return html


def inject_setlang(html: str, t_json: str) -> str:
    js = SETLANG_JS.replace("__T_JSON__", t_json)
    marker = "let tab2Initialized = false;"
    if marker not in html:
        raise SystemExit("tab2Initialized marker missing")
    html = html.replace(marker, js + "\nlet tab2Initialized = false;", 1)

    boot = """
  var initialLang = "en";
  try {
    var saved = localStorage.getItem("courseLang");
    if (saved === "en" || saved === "zh") initialLang = saved;
  } catch(e) {}
  setLang(initialLang);
"""
    html = html.replace(
        "  window.addEventListener('hashchange', function () {",
        boot + "\n  window.addEventListener('hashchange', function () {",
        1,
    )
    return html


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")

    # already-tagged nav keys stay; body tagging:
    reps = [
        ('<span class="coverage full">主題對應</span>', '<span class="coverage full" data-t="cov.full">主題對應</span>'),
        ('<span class="coverage partial">部分覆蓋</span>', '<span class="coverage partial" data-t="cov.partial">部分覆蓋</span>'),
        ('<span class="coverage thin">擦邊</span>', '<span class="coverage thin" data-t="cov.thin">擦邊</span>'),
        ('<span class="coverage none">空白</span>', '<span class="coverage none" data-t="cov.none">空白</span>'),
        ('<span class="gap-tag">最接近</span>', '<span class="gap-tag" data-t="gap.closest">最接近</span>'),
        ('<span class="gap-tag">市場縫隙</span>', '<span class="gap-tag" data-t="gap.gap">市場縫隙</span>'),
        ('<span class="platform-pill">紅海 · 可贏</span>', '<span class="platform-pill" data-t="pill.red">紅海 · 可贏</span>'),
        ('<span class="platform-pill gap">藍海</span>', '<span class="platform-pill gap" data-t="pill.blue">藍海</span>'),
        ('<span class="lesson-title">AI/UX 典範轉移</span>', '<span class="lesson-title" data-t="t1.lesson1">AI/UX 典範轉移</span>'),
        ('<span class="lesson-title">帶領設計師銜接</span>', '<span class="lesson-title" data-t="t1.lesson5">帶領設計師銜接</span>'),
        ('<dt>UI 樣態</dt>', '<dt data-t="dt.ui">UI 樣態</dt>'),
        ('<dt>關鍵限制</dt>', '<dt data-t="dt.limit">關鍵限制</dt>'),
        ('<dt>Prompt 必帶</dt>', '<dt data-t="dt.prompt">Prompt 必帶</dt>'),
        ('<dt>核心角色</dt>', '<dt data-t="cfg.core">核心角色</dt>'),
        ('<dt>Orchestrator</dt>', '<dt data-t="cfg.orch">Orchestrator</dt>'),
        ('<dt>Wiki 切分</dt>', '<dt data-t="cfg.wiki">Wiki 切分</dt>'),
        ('<dt>Harness 壓力</dt>', '<dt data-t="cfg.harness">Harness 壓力</dt>'),
        ('<dt>主要失敗模式</dt>', '<dt data-t="cfg.fail">主要失敗模式</dt>'),
        ('<dt>AI 的角色</dt>', '<dt data-t="cfg.ai">AI 的角色</dt>'),
        ('<dt>Wiki schema 重點</dt>', '<dt data-t="cfg.schema">Wiki schema 重點</dt>'),
        ('<dt>入門第一步</dt>', '<dt data-t="cfg.first">入門第一步</dt>'),
        ("<b>讀</b>", '<b data-t="b.read">讀</b>'),
        ("<b>寫</b>", '<b data-t="b.write">寫</b>'),
    ]
    for old, new in reps:
        html = sub_all(html, old, new)

    unique = [
        ("5 堂課<span class=\"ornament\">×</span>市場對照表", "t1.title"),
        ("把你提案的 5 堂 AI/UX 課對到", "t1.intro"),
        ("5 堂課 × Maven 上最接近的課程", "t1.s1_title"),
        ("以每堂課為列，列出 Maven 上主題最接近的競品。", "t1.s1_desc"),
        ("堂次 / 主題", "t1.th_lesson"),
        ("最接近的 Maven 課程", "t1.th_course"),
        ("講師 / 平台", "t1.th_instr"),
        ("覆蓋深度", "t1.th_cov"),
        ("關鍵差異", "t1.th_diff"),
        ("策略層 UX 如何因 AI 改變", "t1.r1d"),
        ("偏「設計 AI 產品」而非「設計師工作流轉變」", "t1.r1k"),
        ("AI 介面常見問題、agentic UX、AI Design Canvas", "t1.r2d"),
        ("聚焦 pattern library，不談「設計師剩下做什麼」的存在性問題", "t1.r2k"),
        ("策略視角的 AI 整合，從產品策略談 AI 工作流納入", "t1.r3d"),
        ("視角是 PM/Strategist，不是設計師工作流本身", "t1.r3k"),
        ("強調 <strong>behavioral specification</strong>", "t1.r4d"),
        ("切點是「為 AI 產品定義 behavior」", "t1.r4k"),
        ("— 無直接對應 —", "t1.r5title"),
        ("「設計判斷 → 可查詢 / 可引用 / 可版本控管的 markdown 知識庫」", "t1.r5d"),
        ("最強差異點。對應 Karpathy LLM Wiki / Memex 譜系", "t1.r5k"),
        ("Cursor、Claude Code、Stitch、Lovable、Magic Patterns", "t1.r6d"),
        ("工具廣度大，但停在「生成」這一段", "t1.r6k"),
        ("從 Figma 結構（components / variables / auto layout / naming）", "t1.r7d"),
        ("已上線（非開發中），重點在 Figma 結構與 agent handoff", "t1.r7k"),
        ("4 週從 idea 到 ready-to-ship product", "t1.r8d"),
        ("實作導向，較少結構化資料治理", "t1.r8k"),
        ("Claude Code 應用於設計工作流，CLAUDE.md", "t1.r9d"),
        ("沒處理「Red Team 驗收」與「知識回寫」的閉環", "t1.r9k"),
        ("— 完整閉環無對應 —", "t1.r10title"),
        ("「概念生成 → Figma 微調 → repo 固化", "t1.r10d"),
        ("強差異點。對手停在 \"AI 生成 → 設計師覺得不錯 → 交付\"", "t1.r10k"),
        ("Rupa 給主管的單日 workshop", "t1.r11d"),
        ("對象是「個別主管自用」", "t1.r11k"),
        ("Maven UX 主管課組合", "t1.r12d"),
        ("跟 AI 工作流轉型脫鉤，純 UX leadership", "t1.r12k"),
        ("多位講師", "t1.multi"),
        ("Maven · 課程列表", "t1.maven_list"),
        ("— 幾乎沒有對手 —", "t1.r13title"),
        ("「從工具採用 → <strong>知識治理 + 角色重分工 + 工作流成熟度</strong>", "t1.r13d"),
        ("最強差異點。AI/UX 課鎖個人技能，leadership 課避開 AI", "t1.r13k"),
        ('<span class="dot" style="color:var(--accent);">●●●</span> 主題完整對應', "t1.leg1"),
        ('<span class="dot" style="color:var(--accent-soft);">●●○</span> 部分覆蓋', "t1.leg2"),
        ('<span class="dot" style="color:var(--ink-4);">●○○</span> 僅擦邊', "t1.leg3"),
        ('<span class="dot" style="color:var(--ink-4);">○○○</span> 市場空白', "t1.leg4"),
        ("其他平台 × UX 社群", "t1.s2_title"),
        ("Maven 以外的 UX 教育平台、design school", "t1.s2_desc"),
        ("平台 / 講師", "t1.th_plat"),
        ("課程 / 內容", "t1.th_content"),
        ("最相關堂次", "t1.th_rel"),
        ("特點與限制", "t1.th_limit"),
        ("<strong>AI Design Engineering &amp; Vibe Coding</strong>（每月開新班）", "t1.p1c"),
        ("實作為主，沒有 Red Team 與知識回寫；不講管理層", "t1.p1k"),
        ("<strong>AI for UX Design</strong>（4 週）", "t1.p2c"),
        ("較入門；對 MCP / agentic workflow 涵蓋淺", "t1.p2k"),
        ("從 prompts 到 systems 的設計工作流", "t1.p3c"),
        ("主題接近，但 IxDF 風格偏 best-practice 整理，缺實戰閉環", "t1.p3k"),
        ("<strong>AI in UX/UI Design</strong>（自學模組）", "t1.p4c"),
        (">堂 1</span>", "t1.p4rel"),
        ("入門等級；不涉及 MCP / agent / repo", "t1.p4k"),
        ("用 Claude Code 建 content agents 與規範系統", "t1.p5c"),
        (">堂 2</span>", "t1.p5rel"),
        ("切點是 content design system；和你「整體設計知識 repo」鄰近但不同層", "t1.p5k"),
        ("Christine Vallaure（補充寫作）", "t1.vallaure"),
        ("UX Collective 連載 <strong>\"Agentic AI, Design Systems &amp; Figma\"</strong>", "t1.p6c"),
        (">堂 3</span>", "t1.p6rel"),
        ("免費補充教材；Maven 課 (Build Scalable UI) 已上線見堂 3", "t1.p6k"),
        ("<strong>From Figma to Cursor with MCP</strong>（21 分鐘）", "t1.p7c"),
        (">堂 3</span>", "t1.p7rel"),
        ("純工具教學，無理論架構", "t1.p7k"),
        ("Maven 免費 Talks", "t1.maven_talks"),
        ("Perplexity、Flowglad、Henry 等設計師分享 AI 工作流", "t1.p8c"),
        ("免費補充；案例多但無系統化教學", "t1.p8k"),
        ("市場縫隙 × 你的差異點", "t1.s3_title"),
        ("把每堂課的現有市場狀態壓縮成一行", "t1.s3_desc"),
        (">堂次</th>", "t1.th_l"),
        ("現有市場狀態", "t1.th_state"),
        ("你的差異點 / 上位概念", "t1.th_edge"),
        ("市場機會", "t1.th_opp"),
        ("<span class=\"lesson-title\">典範轉移</span>", "t1.s3_l1"),
        ("多堂課都在教「AI 怎麼用」「AI 產品怎麼設計」", "t1.g1s"),
        ("切點是「<strong>設計師作為角色</strong>剩下什麼工作」", "t1.g1e"),
        ("市場上有 prompt library、design system for AI", "t1.g2s"),
        ("把<strong>設計判斷</strong>當成可被 agent 引用的 markdown wiki", "t1.g2e"),
        ("工具教學多到滿出來：Cursor、Lovable、v0、Figma MCP、Claude Code", "t1.g3s"),
        ("切點是「<strong>概念原型 ↔ 結構化資料 ↔ production</strong>」", "t1.g3e"),
        ("現有課程閉環停在「AI 生成 → 人類覺得不錯 → 交付」", "t1.g4s"),
        ("完整 turn = 概念生成 → Figma 微調 → repo 固化", "t1.g4e"),
        ("<span class=\"lesson-title\">主管帶領</span>", "t1.s3_l5"),
        ("AI/UX 課鎖定個人技能；UX leadership 課避開 AI", "t1.g5s"),
        ("命題是「<strong>個人會用 ≠ 團隊具備</strong>」", "t1.g5e"),
        ("如果只能挑一句話定位這門課：", "t1.verdict"),
    ]
    # Fix unique entries that used full tags as content_start — add_dt walks back to opening tag
    # For th "堂次" the content_start ">堂次</th>" would find '>' before 堂次, walking to previous tag. Bad.
    # I'll special-case those below.

    # Filter broken ones and handle separately
    skip_keys = {"t1.p4rel", "t1.p5rel", "t1.p6rel", "t1.p7rel", "t1.th_l", "t1.s3_l1", "t1.s3_l5", "t1.leg1", "t1.leg2", "t1.leg3", "t1.leg4"}
    nth_tracker: dict[str, int] = {}
    for start, key in unique:
        if key in skip_keys:
            continue
        n = nth_tracker.get(start, 0)
        html = add_dt(html, start, key, nth=n)
        nth_tracker[start] = n + 1

    # coverage "堂 N" — unique surrounding
    html = html.replace('<td><span class="coverage">堂 3 / 堂 4</span></td>\n          <td>實作為主',
                        '<td><span class="coverage" data-t="t1.p1rel">堂 3 / 堂 4</span></td>\n          <td>實作為主', 1)
    html = html.replace('<td><span class="coverage">堂 1 / 堂 3</span></td>\n          <td>較入門',
                        '<td><span class="coverage" data-t="t1.p2rel">堂 1 / 堂 3</span></td>\n          <td>較入門', 1)
    html = html.replace('<td><span class="coverage">堂 3 / 堂 4</span></td>\n          <td>主題接近',
                        '<td><span class="coverage" data-t="t1.p3rel">堂 3 / 堂 4</span></td>\n          <td>主題接近', 1)
    html = html.replace('<td><span class="coverage">堂 1</span></td>',
                        '<td><span class="coverage" data-t="t1.p4rel">堂 1</span></td>', 1)
    html = html.replace('<td><span class="coverage">堂 2</span></td>',
                        '<td><span class="coverage" data-t="t1.p5rel">堂 2</span></td>', 1)
    html = html.replace('<td><span class="coverage">堂 3</span></td>\n          <td>免費補充教材',
                        '<td><span class="coverage" data-t="t1.p6rel">堂 3</span></td>\n          <td>免費補充教材', 1)
    html = html.replace('<td><span class="coverage">堂 3</span></td>\n          <td>純工具教學',
                        '<td><span class="coverage" data-t="t1.p7rel">堂 3</span></td>\n          <td>純工具教學', 1)
    html = html.replace('<td><span class="coverage">堂 1 / 堂 3</span></td>\n          <td>免費補充；案例多',
                        '<td><span class="coverage" data-t="t1.p8rel">堂 1 / 堂 3</span></td>\n          <td>免費補充；案例多', 1)

    html = html.replace('<th style="width:160px;">堂次</th>', '<th style="width:160px;" data-t="t1.th_l">堂次</th>', 1)
    html = html.replace('<span class="lesson-title">典範轉移</span>', '<span class="lesson-title" data-t="t1.s3_l1">典範轉移</span>', 1)
    html = html.replace('<span class="lesson-title">主管帶領</span>', '<span class="lesson-title" data-t="t1.s3_l5">主管帶領</span>', 1)
    html = html.replace('<div class="item"><span class="dot" style="color:var(--accent);">●●●</span> 主題完整對應</div>',
                        '<div class="item" data-t="t1.leg1"><span class="dot" style="color:var(--accent);">●●●</span> 主題完整對應</div>', 1)
    html = html.replace('<div class="item"><span class="dot" style="color:var(--accent-soft);">●●○</span> 部分覆蓋</div>',
                        '<div class="item" data-t="t1.leg2"><span class="dot" style="color:var(--accent-soft);">●●○</span> 部分覆蓋</div>', 1)
    html = html.replace('<div class="item"><span class="dot" style="color:var(--ink-4);">●○○</span> 僅擦邊</div>',
                        '<div class="item" data-t="t1.leg3"><span class="dot" style="color:var(--ink-4);">●○○</span> 僅擦邊</div>', 1)
    html = html.replace('<div class="item"><span class="dot" style="color:var(--ink-4);">○○○</span> 市場空白</div>',
                        '<div class="item" data-t="t1.leg4"><span class="dot" style="color:var(--ink-4);">○○○</span> 市場空白</div>', 1)

    # ── tab 2 ──
    t2 = [
        ("設計師日常產出<span class=\"ornament\">×</span>AI 結構化分層", "t2.title"),
        ("把一個典型產品設計專案六個 Sprint 內的 UX 活動全部攤開", "t2.intro"),
        ("純 Markdown · agent-native", "t2.tierA_name"),
        ("有 schema 的結構化文件，可被 agent 查詢、引用、版本控管。", "t2.tierA_desc"),
        ("Markdown 基礎的 html 可視化", "t2.tierB_name"),
        ("prose 主體 + 內嵌 Mermaid / PlantUML / 結構化區塊。", "t2.tierB_desc"),
        ("視覺/空間原生", "t2.tierC_name"),
        ("Figma 是交付hub，過程可以使用 Pencil 作為中介微調", "t2.tierC_desc"),
        ("完整甘特圖", "t2.gantt"),
        ("這 <strong>86% 的 markdown 可結構化文件</strong>", "t2.insight"),
        ("28 種 UX 文件 × 儲存規範", "t2.inv_title"),
        ("用 Gen-AI 把 PRD features 變成多技術棧 variants", "t2.poc_title"),
        ("回到 Gantt 圖上那塊被 ochre 淡色標出的區域", "t2.poc_intro"),
        ("同一 feature × 四種技術棧", "t2.sub31"),
        ("以「<strong>通知管理</strong>」為例", "t2.sub31d"),
        ("原生 App", "t2.ts1"),
        ("iOS / Android Settings 子頁；toggle list；分組", "t2.ts1ui"),
        ("系統層 push 權限、單欄狹窄、touch target ≥ 44pt", "t2.ts1lim"),
        ("響應式網站", "t2.ts2"),
        ("多瀏覽器、無 push（除 Web Push）、breakpoint 行為", "t2.ts2lim"),
        ("SaaS 後台", "t2.ts3"),
        ("role-based defaults、tenant 隔離、audit log 強制", "t2.ts3lim"),
        ("Copilot · 對話優先", "t2.ts4"),
        ("沒有 settings page，靠自然語言設定、smart default", "t2.ts4ui"),
        ("無持久 UI、context window 有限、recall 不可靠", "t2.ts4lim"),
        ("AI Variants 工作流", "t2.sub32"),
        ("Gen-AI 工具的價值不是「一次給對」", "t2.sub32d"),
        ("抽取 feature", "t2.ws1"),
        ("從 PRD 拆出可獨立測試的最小 feature 單位", "t2.ws1b"),
        ("<b>IN</b> · PRD 段落", "t2.ws1io"),
        ("指定技術棧", "t2.ws2"),
        ("明確告訴 AI 是哪一棧 + 主要 viewport", "t2.ws2b"),
        ("<b>OUT</b> · 完整 prompt context", "t2.ws2io"),
        ("生成 N 個 variants", "t2.ws3"),
        ("要求 3–5 個變體，每個走不同 UX 取徑", "t2.ws3b"),
        ("<b>OUT</b> · N 個 prototype", "t2.ws3io"),
        ("對照判準篩選", "t2.ws4"),
        ("不是「哪個漂亮」。對三組判準", "t2.ws4b"),
        ("<b>OUT</b> · 選定 variant + reasoning", "t2.ws4io"),
        ("寫進決策日誌", "t2.ws5"),
        ("把「為什麼選 B 不選 A」寫進", "t2.ws5b"),
        ("<b>OUT</b> · immutable 紀錄", "t2.ws5io"),
        ("四個常見誤區", "t2.sub33"),
        ("POC 階段最容易出錯的，不是 AI 生成本身", "t2.sub33d"),
        ("誤區", "t2.th_pit"),
        ("症狀", "t2.th_sym"),
        ("修正", "t2.th_fix"),
        ("沒指定技術棧", "t2.pf1"),
        ("AI 給出 web 樣式 + mobile gesture + admin table 拼貼的「四不像」", "t2.pf1s"),
        ("Prompt 開頭必寫 <code>platform + primary viewport + design system</code>", "t2.pf1f"),
        ("variants 都覺得不錯", "t2.pf2"),
        ("陷入「再生一輪試試」的循環，選不出來", "t2.pf2s"),
        ("生成前先寫好 <code>3 條 selection criteria</code>", "t2.pf2f"),
        ("variants 當交付物", "t2.pf3"),
        ("直接把 AI variant 丟進 Figma，工程師發現邏輯破洞回頭重做", "t2.pf3s"),
        ("variants 只是材料；只挑 <code>1 個進 Figma</code>", "t2.pf3f"),
        ("不寫選擇理由", "t2.pf4"),
        ("三週後同樣決策又要再來一次", "t2.pf4s"),
        ("第 5 步是強制 gate；沒 <code>decision log</code>", "t2.pf4f"),
        ("POC 階段<br>\n              的本質", "t2.poc_lab"),
        ("POC 階段的本質是「<strong>用 AI 製造可比較的選項，用設計師的判斷收斂</strong>」", "t2.poc_body"),
    ]
    for start, key in t2:
        html = add_dt(html, start, key)

    # ── tab 3 ──
    t3 = [
        ("策展與編排", "t3.title"),
        ("C1 結束在一句話：", "t3.intro"),
        ("譜系 · Memex → LLM Wiki → UX Dataset Repository", "t3.s1_title"),
        ("Vannevar Bush 1945 年想做的、Andrej Karpathy 最近重啟的", "t3.s1_desc"),
        ("私有、被<strong>主動策展</strong>的知識庫。", "t3.ped1"),
        ("把 Memex 接上 LLM：<strong>humans curate sources, AI handles summarizing, cross-referencing, filing</strong>", "t3.ped2"),
        ("分層：raw sources · wiki pages · schema", "t3.ped2q"),
        ("LLM Wiki 在<strong>產品設計領域</strong>的特化", "t3.ped3"),
        ("把 C1 的 86% Tier A+B 文件當作可被 agent 引用的知識基礎", "t3.ped3q"),
        ("三欄架構 · AI/UX Writing 的 CoT 如何編排多 Agent", "t3.s2_title"),
        ("左欄是<strong>不可變的原始素材</strong>", "t3.s2_desc"),
        ("產品規格 / 功能清單", "t3.svg_prd"),
        ("使用者旅程", "t3.svg_journey"),
        ("模塊清單", "t3.svg_mod"),
        ("頁面清單", "t3.svg_page"),
        ("使用者流程", "t3.svg_flow"),
        ("分類目錄", "t3.svg_cat"),
        ("時序記錄", "t3.svg_log"),
        ("主題頁面", "t3.svg_pages"),
        ("cross-ref 慣例 · 檔名規範 · lint 規則 · voice &amp; tone", "t3.svg_schema"),
        ("改 schema 比改每個頁面有效", "t3.svg_schema2"),
        ("畫 UI · 產 prototype", "t3.svg_ag1"),
        ("訪談 · 產 insight", "t3.svg_ag2"),
        ("UX 微文案 · voice", "t3.svg_ag3"),
        ("矛盾 · 對抗檢查", "t3.svg_ag4"),
        ("原始素材 immutable，永遠不改寫。", "t3.cap1"),
        ("三層：catalog (<code>index.md</code>)", "t3.cap2"),
        ("四個專責 worker + 一個 Orchestrator。", "t3.cap3"),
        ("MarkItDown 是入場券，不是答案", "t3.s3_title"),
        ("上圖 INGEST 那條 rust dashed line", "t3.s3_desc"),
        ("MarkItDown <b>解決的部分</b>", "t3.md_does"),
        ("純格式轉換 · commodity infrastructure", "t3.md_does_sub"),
        ("把 <code>.pdf</code> / <code>.docx</code> / <code>.pptx</code> / <code>.xlsx</code> 轉成乾淨 markdown", "t3.md_d1"),
        ("圖片做 OCR + EXIF metadata 抓取", "t3.md_d2"),
        ("音訊做 speech transcription（會議錄音 → 逐字稿）", "t3.md_d3"),
        ("HTML / CSV / JSON / XML / EPub / YouTube URL 一鍵 ingest", "t3.md_d4"),
        ("內建 <code>markitdown-mcp</code> server，可直接掛 Claude Desktop / Claude Code", "t3.md_d5"),
        ("Plugin 架構，可寫自訂 converter（之後 Figma 匯出可走這條）", "t3.md_d6"),
        ("MarkItDown <b>不解決的部分</b>", "t3.md_dont"),
        ("設計知識架構 · curator 的核心判斷", "t3.md_dont_sub"),
        ("不會 <strong>summarize</strong>（Karpathy LLM Wiki 的核心動作）", "t3.md_n1"),
        ("不會建 <strong>cross-reference</strong>（不同文件間的實體對齊）", "t3.md_n2"),
        ("不會 <strong>file / categorize</strong>", "t3.md_n3"),
        ("不會生 <code>index.md</code> / <code>log.md</code>", "t3.md_n4"),
        ("不懂 <strong>schema / frontmatter / naming convention</strong>", "t3.md_n5"),
        ("不認識「設計知識」——它不知道 page list 和 user flow 在語意上是不同物件", "t3.md_n6"),
        ("— 失真風險：MarkItDown 跑得過、但設計知識被掏空的四種情境", "t3.dist_h"),
        ("<strong>convert ≠ understand</strong>。下面四種來源是教學上最容易被忽略的陷阱", "t3.dist_d"),
        ("來源類型", "t3.th_src"),
        ("MarkItDown 處理後的狀態", "t3.th_after"),
        ("設計知識的損失", "t3.th_loss"),
        ("Curator 必須補的", "t3.th_patch"),
        ("Figma 匯出 PDF", "t3.d1s"),
        ("圖被 OCR 或變 base64 embed", "t3.d1a"),
        ("元件結構、tokens、variants 全失", "t3.d1l"),
        ("流程圖 / wireframe", "t3.d2s"),
        ("圖片轉描述性文字（OCR）", "t3.d2a"),
        ("空間關係、連線意義消失", "t3.d2l"),
        ("手寫 Mermaid 或 frontmatter 補連線語意", "t3.d2p"),
        ("會議錄音", "t3.d3s"),
        ("逐字稿（含時間戳）", "t3.d3a"),
        ("誰主張什麼、誰反駁——需手工 markup", "t3.d3l"),
        ("複雜版面 Word", "t3.d4s"),
        ("主結構保留，註解 / 修訂紀錄常掉", "t3.d4a"),
        ("side comments、track changes 不見", "t3.d4l"),
        ("手動把關鍵 comment 抽到 page bottom", "t3.d4p"),
        ("從 raw markdown 到 LLM Wiki：策展三件事", "t3.s4_title"),
        ("把 MarkItDown 出來的 raw markdown 變成 agent 讀得懂的 LLM Wiki", "t3.s4_desc"),
        ("加 frontmatter 規範", "t3.c1n"),
        ("為每種文件類型（persona、use case、decision、page）定義 YAML frontmatter schema", "t3.c1b"),
        ("建 backlinks 與 tags", "t3.c2n"),
        ("<strong>單一 markdown 是孤島</strong>", "t3.c2b"),
        ("<b>IN</b> · 一份孤立的 markdown", "t3.c2e"),
        ("寫進 index.md / log.md", "t3.c3n"),
        ("<code>index.md</code> 是分類目錄（agent 用它導航）", "t3.c3b"),
        ("<b>IN</b> · 新增的 wiki page", "t3.c3e"),
        ("範例 · WORKED EXAMPLE", "t3.ex_mark"),
        ("cross-ref 怎麼讓 agent 串起四份文件", "t3.ex_title"),
        ("<strong>場景：</strong>有人問 agent「為什麼 notification-prefs 頁面的預設模式是 digest？」", "t3.ex_intro"),
        ("↓ 順著 <code>implements</code> 跳到對應的 decision", "t3.jump1"),
        ("↓ 順著 <code>applies_to_personas</code> 跳到 persona", "t3.jump2"),
        ("trade_off: digest 損失即時性，換取留存率", "t3.pre2"),
        ("pain: noise (99% 的通知不重要)", "t3.pre3"),
        ("<strong>Agent 答覆：</strong>因為核心 persona Sarah 的痛點是 noise", "t3.ans"),
        ("這條從 <strong>page → decision → persona</strong> 的追蹤路徑", "t3.close"),
        ("Orchestrator = YOU · 設計師的疊加身份", "t3.s5_title"),
        ("Wiki 建起來，agent 就有可以引用的 context。但 agent 不會自己決定", "t3.s5_desc"),
        ("畫 UI、產 prototype、Figma 操作。C1 講的 POC variants 由它跑。", "t3.ag1"),
        ("訪談轉錄、insight 萃取、persona 更新建議。", "t3.ag2"),
        ("UX 微文案、tone & voice 一致性檢查、多語對齊。", "t3.ag3"),
        ("找矛盾、跑對抗檢查、edge case 暴露。C4 的核心。", "t3.ag4"),
        ("決定誰先跑、誰餵誰、什麼時候 merge、什麼時候打回。用 CoT 寫作做策展。", "t3.ag5"),
        ("CoT · 決策 · 編排腳本", "t3.ag5r"),
        ("現在你有 <strong>Wiki</strong>、有 <strong>Agents</strong>、有 <strong>Orchestrator</strong>。", "t3.bridge"),
        ("<strong>規劃中</strong>：從概念原型到結構化設計流轉。", "t4.intro"),
    ]
    for start, key in t3:
        html = add_dt(html, start, key)

    # ── tab 6 ──
    t6 = [
        ("把整套系統<span class=\"ornament\">×</span>交付給團隊", "t6.title"),
        ("C1 給你 86% 結構化的判斷、C2 給你 wiki + agents + orchestrator、C3 給你 dialectic loop。", "t6.intro"),
        ("從 C1-C3 收網：個人尺度 → 團隊尺度", "t6.s1_title"),
        ("把三章建構物攤平：你已經把整套系統建出來了", "t6.s1_desc"),
        ("典範轉移", "t6.rc1n"),
        ("86% UX 文件可結構化、POC variants 紀律、補完 spec 是設計師的本體工作。", "t6.rc1b"),
        ("個人 · 一個 feature", "t6.rc1s"),
        ("Wiki 三欄 + 4 agents + Orchestrator + curation 三件事", "t6.rc2b"),
        ("個人 · 一份 wiki", "t6.rc2s"),
        ("正反合三節拍 + Red Team 必經 + 寫回 wiki 才算閉環。", "t6.rc3b"),
        ("個人 · 一個 round", "t6.rc3s"),
        ("把 C1-C3 交付給團隊——harness 五層壓縮治理", "t6.rc4b"),
        ("團隊 · 持續運作", "t6.rc4s"),
        ("回頭看 CoT 通用介面圖：哪些 node 還沒收", "t6.s2_title"),
        ("從 V5 的 force-directed graph 把六種 node 攤平盤點。", "t6.s2_desc"),
        ("<code>CoT · markdown</code> 一直被使用，但從沒被當成命題講出口。", "t6.inv1"),
        ("PM Designer / UR / UI / Visual / Orchestrator——C2 塌縮成一個", "t6.inv2"),
        ("Design / Research / Copy / Red Team——C2 完整覆蓋", "t6.inv3"),
        ("Raw · Pages · Schema · index · log · cross-ref——C2 三欄架構", "t6.inv4"),
        ("L1-L5 壓縮 + Model View + Persistent View——C1-C3 完全沒碰。", "t6.inv5"),
        ("Gen-AI · POC · 默會 · Antigravity · Pencil · Red Team 驗收", "t6.inv6"),
        ("Harness 五層壓縮映射到設計工作流", "t6.s3_title"),
        ("Harness 原本是 LLM agent 工程的概念——管 context window", "t6.s3_desc"),
        ("Harness Op (LLM 語境)", "t6.th_hop"),
        ("設計工作流的對應", "t6.th_map"),
        ("移除重複訊息", "t6.h1e"),
        ("<strong>同 feature 多份重複 spec / design review notes 合併。</strong>", "t6.h1m"),
        ("摘要工具輸出", "t6.h2e"),
        ("<strong>user research notes → persona / scenario page。</strong>", "t6.h2m"),
        ("合併對話輪次", "t6.h3e"),
        ("<strong>sprint 內多次 design crit 合併成單一 decision。</strong>", "t6.h3m"),
        ("生成全局摘要", "t6.h4e"),
        ("<strong>sprint retrospective + 下 sprint kickoff brief。</strong>", "t6.h4m"),
        ("截斷最舊記錄", "t6.h5e"),
        ("<strong>把舊 decisions 搬到 <code>archive/</code>（不刪除）。</strong>", "t6.h5m"),
        ("模型這輪看到的", "t6.h6e"),
        ("<strong>當 sprint 的工作 context</strong>", "t6.h6m"),
        ("完整任務歷史", "t6.h7e"),
        ("<strong>整個 wiki + archive</strong>", "t6.h7m"),
        ("Harness 不是 agent 工程師才需要懂的東西——", "t6.h_ins"),
        ("一人 PD（NA-style） · 分工團隊（亞洲 style）", "t6.s4_title"),
        ("北美的 Product Designer 角色是一人扛多職", "t6.s4_desc"),
        ("配置 A", "t6.cfgA"),
        ("一人 Product Designer", "t6.cfgAh"),
        ("一人扛 <strong>research / IA / UI / interaction / 微文案</strong> 全部", "t6.cfgA_core"),
        ("就是你自己", "t6.cfgA_orch"),
        ("個人 scratchpad + 對工程的 handoff doc。", "t6.cfgA_wiki"),
        ("<strong>低</strong>——一顆腦、一個 context、單一 voice", "t6.cfgA_h"),
        ("判斷力疲勞、scope creep、", "t6.cfgA_f"),
        ("<strong>force multiplier</strong>——讓你以 5 倍速跑所有 role 的工作", "t6.cfgA_ai"),
        ("個人 voice + 簡 frontmatter 即可；重點放", "t6.cfgA_s"),
        ("<code>personal wiki</code> + Claude Code（1-2 週可建起）", "t6.cfgA_1"),
        ("配置 B", "t6.cfgB"),
        ("分工團隊", "t6.cfgBh"),
        ("亞洲 style · explicit role split", "t6.cfgB_tag"),
        ("<strong>PM Designer + UR + UI Designer + Visual + 文案</strong>，各自獨立職能", "t6.cfgB_core"),
        ("Lead designer 或 design manager（不是 PM）", "t6.cfgB_orch"),
        ("各 role own 各自切片——", "t6.cfgB_wiki"),
        ("<strong>高</strong>——multiple agents 同時跑", "t6.cfgB_h"),
        ("知識孤島、跨 role 決策衝突、", "t6.cfgB_f"),
        ("<strong>glue between role boundaries</strong>——補角色之間的縫", "t6.cfgB_ai"),
        ("strict schema + <code>owner</code> 欄位 + 跨 role 強制 link", "t6.cfgB_s"),
        ("Cross-role <strong>schema workshop</strong>（1 週）", "t6.cfgB_1"),
        ("<strong>關鍵命題</strong>：這兩種配置都用同一套（wiki + agents + harness）系統。", "t6.s4_claim"),
        ("CoT 作為通用介面 · 整個課程的論點命題化", "t6.s5_title"),
        ("到 C4 的這一節，整個課程的核心論點才被正面說出來：", "t6.s5_desc"),
        ("— 拿掉 CoT，圖就散了。整張圖的內聚力只來自這個 hub。", "t6.svg_foot"),
        ("<strong>所有節點被拉向同一個中心：markdown · CoT 寫作。</strong>", "t6.hub"),
        ("— 為什麼這個 hub 重要：五條 compose 軸線", "t6.axis_h"),
        ("其他 AI/UX 工作流方案綁定特定工具或特定 platform", "t6.axis_d"),
        ("i · 跨 ROLES", "t6.cb1a"),
        ("通用書寫介面", "t6.cb1t"),
        ("UR / UI / Visual / 文案都用 markdown，介面通用", "t6.cb1b"),
        ("ii · 跨 AGENTS", "t6.cb2a"),
        ("通用 context format", "t6.cb2t"),
        ("Design / Research / Copy / Red Team 都吃 markdown context", "t6.cb2b"),
        ("iii · 跨 TOOLS", "t6.cb3a"),
        ("viewer 可替換", "t6.cb3t"),
        ("Obsidian / VS Code / Cursor / Claude Code / GitHub web 都讀 markdown", "t6.cb3b"),
        ("iv · 跨 TEAMS", "t6.cb4a"),
        ("配置可演化", "t6.cb4t"),
        ("Solo PD 跟 split team 用同一 substrate，可漸進演化", "t6.cb4b"),
        ("v · 跨 TIME", "t6.cb5a"),
        ("Git 即歷史", "t6.cb5t"),
        ("Git 紀錄 markdown 變更歷史；5 年後新人 onboarding", "t6.cb5b"),
        ("五級成熟度 × 兩種團隊配置的入門路徑", "t6.s6_title"),
        ("把整門課的 deliverable 拉成五級成熟度", "t6.s6_desc"),
        ("個人 AI 工具使用者 <span class=\"mat-name-tag\">課前狀態</span>", "t6.m0n"),
        ("用 ChatGPT / Cursor 提速個人產出，沒有 wiki，", "t6.m0c"),
        ("「我會用 ChatGPT」「我用 v0 跑了一個 prototype」", "t6.m0i"),
        ("建 personal wiki（1-2 sprint）", "t6.m0p"),
        ("個人 wiki + 簡單 agents <span class=\"mat-name-tag\">C2 末</span>", "t6.m1n"),
        ("有結構化 markdown wiki，1-2 個 agents 跑特定任務。", "t6.m1c"),
        ("「我的設計決策現在寫在 wiki 裡，不只在我腦袋」", "t6.m1i"),
        ("引入 Red Team agent（next 1-2 sprint）", "t6.m1p"),
        ("Dialectic loop 紀律 <span class=\"mat-name-tag\">C3 末</span>", "t6.m2n"),
        ("每個 feature 走完 thesis-antithesis-synthesis，", "t6.m2c"),
        ("「我沒讓 Red Team 跑過就不算這個 feature 處理完」", "t6.m2i"),
        ("harness 壓縮策略整理 wiki（3-6 months）", "t6.m2p"),
        ("Harness governance + 多角色分工治理 <span class=\"mat-name-tag\">C4 主目標</span>", "t6.m3n"),
        ("<strong>五層壓縮策略對應 sprint cadence、cross-role schema 統一、Model View / Persistent View 邊界清晰</strong>", "t6.m3c"),
        ("「我們每 2 週做 global summary 寫進 log.md", "t6.m3i"),
        ("通常停在這層（個人尺度的終點）", "t6.m3p"),
        ("跨團隊 CoT 紀律 <span class=\"mat-name-tag\">後續方向</span>", "t6.m4n"),
        ("<strong>整個 design org 用同一套 substrate</strong>", "t6.m4c"),
        ("「新組成立第一週做的事是 fork wiki schema」", "t6.m4i"),
        ("不適用（你還是一個人）", "t6.m4p"),
        ("四章走完，整個論點圖完成：", "t6.finale"),
    ]
    for start, key in t6:
        html = add_dt(html, start, key)

    # Extract T.zh from tagged nodes
    soup = BeautifulSoup(html, "html.parser")
    zh: dict[str, str] = dict(ZH_OVERRIDE)
    for el in soup.select("[data-t]"):
        key = el.get("data-t")
        if key in ZH_OVERRIDE:
            continue
        inner = el.decode_contents()
        if key in zh and zh[key] != inner:
            # same key, identical expected
            pass
        zh[key] = inner

    missing_en = sorted(set(zh) - set(EN))
    extra_en = sorted(set(EN) - set(zh) - set(ZH_OVERRIDE))
    if missing_en:
        print("MISSING EN:", len(missing_en))
        for k in missing_en:
            print(" ", k, "=>", zh[k][:80].replace("\n", " "))
        raise SystemExit("fill EN for missing keys")
    if extra_en:
        print("EXTRA EN (ok if unused):", extra_en)

    t_obj = {"en": EN, "zh": {**EN, **zh}}
    # zh should win for all extracted keys
    t_obj["zh"] = {k: zh.get(k, EN[k]) for k in EN}
    # also include any zh-only? shouldn't

    t_json = json.dumps(t_obj, ensure_ascii=False, separators=(",", ":"))
    html = patch_gantt(html)
    if "function setLang" not in html:
        html = inject_setlang(html, t_json)
    else:
        print("setLang already present — skip inject")

    HTML_PATH.write_text(html, encoding="utf-8")
    print("Wrote", HTML_PATH)
    print("EN keys:", len(EN), "ZH keys:", len(t_obj["zh"]))
    print("data-t count in file:", html.count("data-t="))


if __name__ == "__main__":
    main()
