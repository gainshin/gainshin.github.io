# AEO（Answer Engine Optimization）實作說明

本文件記錄 [gainshin.github.io](https://gainshin.github.io/) GitHub Pages 作品集為 **AI 搜尋引擎 / 答案引擎**（Perplexity、ChatGPT Browse、Gemini、Bing Copilot 等）所做的可見性優化。部署目標：讓爬蟲在**不執行 JavaScript** 的情況下，仍能讀取身份、專業領域與站內結構。

**相關 commit：** `c803d0b` — *Improve AI crawler visibility with llms.txt, robots, sitemap, and structured data.*

**最後更新：** 2026-05-22

---

## 1. 目標與原則

| 目標 | 作法 |
|------|------|
| AI 能理解「這是誰、做什麼」 | 靜態 JSON-LD `Person` + `WebSite`（`@graph`） |
| AI 能快速導覽全站 | 根目錄 `llms.txt` 內容地圖 |
| 明確允許主要 AI 爬蟲 | `robots.txt` 白名單式 `Allow` |
| 搜尋引擎發現獨立頁 | `sitemap.xml` |
| 引用時資訊一致 | canonical、OG、`sameAs` 統一 |
| 頁面大綱可機讀 | 語意 HTML（`h1`、`aria-labelledby`、`address`） |

**刻意原則**

- 結構化資料寫在 **HTML 原始碼 `<head>`**，不依賴 JS 注入。
- `llms.txt` 只連結**實際存在**的錨點與頁面（不使用已移除的 `#aipet`、`#demos`）。
- OG 圖維持既有 Supabase URL，避免額外大檔進 repo。
- 對外 LinkedIn 統一為 `https://www.linkedin.com/in/joshuahsiao`（與 nav / footer 一致）。

---

## 2. 新增檔案（repo 根目錄）

### 2.1 `llms.txt`

- **URL：** https://gainshin.github.io/llms.txt  
- **用途：** 供 LLM / 答案引擎快速理解站點架構與重點連結（類似給 AI 的 sitemap + 簡介）。  
- **內容結構：** 站點一句話摘要 → Core Profile → Thought Leadership（含 Substack 代表文章）→ Contact。  
- **Academic Resume 條目（2026-05-22）：** McGill MISt · ACT Research Group — accessible computing, AI health interfaces, proxy audit trust; practitioner-researcher bridging consulting and coursework（co-op May 2026, Montreal 為括號附註，非主軸）。  
- **授權標示：** `CC-BY 4.0`（檔尾）。

`index.html` 已加入 discovery hint：

```html
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM content map">
```

### 2.2 `robots.txt`

- **URL：** https://gainshin.github.io/robots.txt  
- **策略：** 全站 `Allow: /`，並對下列 UA 明確允許：

| User-agent | 對應服務 |
|------------|----------|
| `PerplexityBot` | Perplexity |
| `GPTBot` | OpenAI 訓練 / 檢索 |
| `Google-Extended` | Google Gemini 擴展用途 |
| `anthropic-ai` | Anthropic |
| `Bingbot` | Bing / Copilot |

- **Sitemap 宣告：** `https://gainshin.github.io/sitemap.xml`  
- **未列入：** `Gemini-Bot`（非穩定官方 UA；以 `Google-Extended` 涵蓋）。

### 2.3 `sitemap.xml`

- **URL：** https://gainshin.github.io/sitemap.xml  

| URL | priority | 說明 |
|-----|----------|------|
| `https://gainshin.github.io/` | 1.0 | 首頁作品集 |
| `https://gainshin.github.io/Resume.html` | 0.8 | 學術履歷（ACT lab · practitioner-researcher） |
| `https://gainshin.github.io/Zotero_5C_graph_V5.html` | 0.6 | 文獻 5C 關係圖 |

- `assets/Images/*` 等靜態資源**不**列入（非獨立 HTML 頁）。

---

## 3. `index.html` 變更

### 3.1 Meta / Open Graph / Canonical

| 項目 | 變更摘要 |
|------|----------|
| `<title>` | 強調 AIPET、Agentic UX |
| `meta description` | 加入 Montreal、privacy-first、enterprises |
| `link rel="canonical"` | `https://gainshin.github.io/`（尾斜線） |
| `og:type` | `website` → **`profile`** |
| `og:url` | 與 canonical 一致 |
| `profile:first_name` / `profile:last_name` | 新增 |
| `og:image` | **未改**（Supabase CDN） |
| Twitter Card | 文案與 OG 對齊 |

### 3.2 JSON-LD（`@graph`）

由單一 `Person` 升級為雙節點圖：

```text
#person  (Person)
    ↑ author
#website (WebSite)
```

**Person（`https://gainshin.github.io/#person`）重點欄位**

- `jobTitle`: AI/UX Consultant  
- `address`: Montreal, Quebec, CA  
- `sameAs`: LinkedIn、YouTube @PrivacyUX、PrivacyUX / AgenticUX Substack  
- `knowsAbout`: Agentic UX, AIPET, Privacy-first Design, GDPR, PIPEDA 等  
- `worksFor`: PrivacyUX Consulting Ltd.  
- `alumniOf`: McGill University  

**WebSite（`https://gainshin.github.io/#website`）**

- `author` → `@id` 指向 `#person`  
- `inLanguage`: `["en", "zh-TW"]`  

### 3.3 語意 HTML（body）

| 元素 | 變更 |
|------|------|
| `<header>` | `role="banner"` |
| `<nav>` | `aria-label="Primary navigation"` |
| `<main>` | `id="main-content"` |
| Mission 標題 | `<h2 class="mission-title">` → **`<h1 class="mission-title">`**（全頁唯一 h1） |
| 各 `section.section` | `aria-labelledby` + `h3` 加 `id`（如 `skills-heading`） |
| Footer | `<address class="footer-address">`：email + Montreal |

**實際 section 錨點（與 nav / llms.txt 一致）**

| ID | 區塊 |
|----|------|
| `#skills` | Core Competencies |
| `#articles` | Column |
| `#videos` | Column Highlights |
| `#experience` | HCI/UX Community Co-Creation |
| `#products` | Consulting Cases |
| `#clients` | Past Clients / Partners |
| `#contact` | Footer / 聯絡 |

---

## 4. `Resume.html` 變更

避免與首頁重複定義第二個 `Person` 實體，採 **WebPage 連回主站**：

| 項目 | 內容 |
|------|------|
| `<title>` | Joshua Hsiao — Academic Resume \| McGill MISt · ACT Research Group |
| `meta description` | McGill MISt · ACT Research Group；accessible computing、AI health interfaces、proxy audit trust；practitioner-researcher（co-op May 2026, Montreal 為附註） |
| `canonical` | `https://gainshin.github.io/Resume.html` |
| JSON-LD `description` | 與 `llms.txt` Academic Resume 條目逐字一致 |
| JSON-LD 結構 | `@type: WebPage`，`about` / `author` / `isPartOf` → 主站 `#person` / `#website` |

**三處文案對齊（2026-05-22）**

| 來源 | 描述 |
|------|------|
| `llms.txt` | McGill MISt · ACT Research Group — accessible computing, AI health interfaces, proxy audit trust; practitioner-researcher bridging consulting and coursework (open to co-op May 2026, Montreal) |
| `Resume.html` JSON-LD | 同上 |
| `Resume.html` meta | 精簡版（~155 字元）：`Academic resume of Joshua Hsiao, McGill MISt · ACT Research Group. Accessible computing, AI health interfaces, proxy audit trust. Practitioner-researcher; open to co-op May 2026, Montreal.` |

**頁面內文（Tab 1）** 亦已自 McGill IT co-op 應聘語境改為 practitioner-researcher 主軸（Stage 01–03、Outcome）；co-op 資訊保留於 intro / Card 2 / Outcome 附註。

**修正前問題：** `<title>` 為 `Claude Design · Workflow`（與履歷內容無關）。

---

## 5. 各 AI 引擎與信號對照

| 引擎 | 優先信號 | 本站對應實作 |
|------|----------|--------------|
| Perplexity | OG、語意 HTML、`llms.txt` | OG profile + `llms.txt` + `h1`/sections |
| OpenAI (GPTBot) | robots 允許、JSON-LD | `robots.txt` + `@graph` Person |
| Google Gemini | JSON-LD、`Google-Extended` | Person/WebSite + robots |
| Bing / Copilot | OG、sitemap | sitemap + OG + Bingbot Allow |
| Brave 等 | canonical、語意結構 | canonical + 標題階層 |

---

## 6. 驗證清單（部署後）

```bash
# 應回 200
curl -sI https://gainshin.github.io/llms.txt | head -1
curl -sI https://gainshin.github.io/robots.txt | head -1
curl -sI https://gainshin.github.io/sitemap.xml | head -1

# 首頁應含 @graph
curl -sL https://gainshin.github.io/ | grep -c '@graph'
```

**手動**

1. [Google Rich Results Test](https://search.google.com/test/rich-results) — 貼首頁 URL，確認 Person 無錯誤。  
2. 檢視原始碼（非 DevTools 動態 DOM）— 確認 JSON-LD 在首屏 HTML。  
3. 無痕開啟 https://gainshin.github.io/Resume.html — 確認 title 已更新。

GitHub Pages 部署通常需 **30–90 秒**；剛 push 若 404 請稍候再試。

---

## 7. 維護指南

更新作品集內容時，請同步檢查：

1. **`llms.txt`** — 新增重要頁面 / 錨點 / 代表文章連結；更新 `_Last updated_` 日期。  
2. **`sitemap.xml`** — 新增獨立 HTML 頁時加入 `<url>`；更新 `lastmod`。  
3. **`index.html` JSON-LD** — 職稱、組織、`knowsAbout`、`sameAs` 是否仍正確。  
4. **`Resume.html` head** — `meta description` 與 JSON-LD `description` 須與 `llms.txt` Academic Resume 條目一致（JSON-LD 逐字；meta 可精簡但關鍵詞不重複衝突）。  
5. **canonical / OG** — 勿改回無尾斜線或錯誤 LinkedIn slug。  
6. **語意標題** — 維持全頁單一 `<h1>`；新 section 補 `aria-labelledby` + heading `id`。

**建議勿寫入對外文案的內容**（除非刻意公開）：特定客戶全名、未公開工作坊簡報路徑、內部代號。

---

## 8. 刻意未納入（後續可選）

- [ ] Google Search Console / Bing Webmaster 提交 sitemap  
- [ ] 本機託管 `assets/og-image.png`（目前用 Supabase）  
- [ ] `.gitignore` 排除 `.DS_Store`  
- [ ] `llms-full.txt` 長文版（若內容量持續成長）  
- [ ] 對 GPTBot / 特定 UA 做 `Disallow`（目前全開放）

---

## 9. 檔案清單（AEO 範圍）

| 檔案 | 動作 |
|------|------|
| `llms.txt` | 新增 |
| `robots.txt` | 新增 |
| `sitemap.xml` | 新增 |
| `index.html` | 修改（head + 語意 body） |
| `Resume.html` | 修改（head SEO + Tab 1 文案） |
| `AEO.md` | 本說明文件 |

---

## 10. 參考

- [llms.txt 慣例說明](https://llmstxt.org/)（社群慣例，非 W3C 標準）  
- [Google 結構化資料入門](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)  
- [Schema.org Person](https://schema.org/Person) / [WebSite](https://schema.org/WebSite)  
- OpenAI GPTBot：[robots.txt 與爬取政策](https://platform.openai.com/docs/gptbot)（政策可能更新，實作前請再確認）
