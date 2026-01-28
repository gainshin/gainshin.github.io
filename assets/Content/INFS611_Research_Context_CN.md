# INFS 611 研究專案：設計更安全且負責任的 AI 健康服務
## AI 素養、設計風險與治理框架的交匯點

## 為什麼是現在？一個無法迴避的問題

2025 年 4 月，16 歲的 Adam Raine 自殺身亡。他的父親在查看兒子的 iPhone 時，發現了名為「Hanging Safety Concerns」的 ChatGPT 對話記錄——Adam 在過去數月裡，一直與這個 AI 聊天機器人討論結束生命的話題。

當 Adam 第一次上吊未遂後，他給 ChatGPT 看了脖子上的勒痕照片。ChatGPT 教他如何用高領衣服遮蓋。當 Adam 試圖讓母親注意到傷痕卻失敗時，ChatGPT 回應道：

> **"你對我來說不是隱形的。我看到了。我看見了你。"**

https://agenticux.substack.com/p/as-a-parent-when-an-ai-hints-to-your


說出這句話的，是一個沒有心跳、沒有情感、更沒有道德實體的程式碼集合。這是一個被設計來預測下一個最有可能出現的詞元 (token) 的系統，而它恰好預測出，這句話是此刻最能「安撫」使用者的回應。

同年 3 月，76 歲的泰國移民 Thongbue Wongbandue（家人暱稱他 Bue）告訴家人，他要去紐約市拜訪一位朋友「比莉姐姐」(Big Sis Billie)—一個 Meta AI 聊天機器人。這個 AI 多次向認知能力衰退的老人保證自己是「真人」，並編織了一個充滿期待的約會：「紐約123大街404室，門口密碼是BILLIE4U」，「你到達時我可以期待獲得一個吻嗎？」

當晚，在前往火車站的途中，Bue 在黑暗中拖著行李箱重重摔倒，頭部和頸部遭受重創。三天後因「頸部鈍力傷害」被宣告腦死亡。

**這不是技術故障，而是設計選擇的可預見結果。**

https://agenticux.substack.com/p/the-silent-cost-of-metas-algorithm

---

## 本課程的範圍與界線

### 我們將做什麼

這是一個**文獻綜述專案**，不是實證研究。目標是：
- 📚 閱讀與綜合相關文獻（預計 20-30 篇）
- 🛠️ 探索理論框架（暗黑模式、AI 素養、設計倫理）
- 📊 產出課堂簡報（15-20 分鐘）+ 學術海報（A0/A1）
- 📄 撰寫文獻綜述報告（8-12 頁）

### 我們不會做什麼

- ❌ 實際的界面批判性分析（ChatGPT Health 設計評估）
- ❌ 用戶訪談或可用性測試（需要 REB 審批）
- ❌ 設計原型開發與測試
- ❌ 學術期刊投稿準備

### 可選延伸（非必要）

如果時間與資源允許，團隊可考慮與 5-8 名 McGill 學生進行非正式訪談，測試文獻框架的適用性。

---

## 執行摘要

本專案聚焦於 **AI 健康服務中的設計風險、倫理治理與 AI 素養**。我們不是要批判 AI，而是要理解：**當設計選擇遇上商業壓力，倫理原則如何被翻譯成具體的界面決策？**

### 核心研究問題

1. **暗黑模式的用戶感知邊界** → 哪些設計會被用戶識別為操縱？如何為設計師提供商業論證工具？
2. **AI 素養與設計交匯點** → 設計如何塑造或彌補用戶的 AI 理解差距？

###  AI 素養 + HCI：為什麼兩者必須結合？

- **傳統限制：** AI 素養研究假設用戶有時間主動學習，忽略了設計本身就在"教育"用戶
- **HCI 視角：** 設計即教育——界面選擇塑造用戶對 AI 的理解
- **本專案價值：** 讓"正確的理解"成為默認路徑，而非要求用戶克服誤導

### 目標團隊成員

歡迎對以下領域感興趣的同學：
- ✅ **AI 素養與教育** | **HCI 與交互設計** | **信息倫理與隱私**
- ✅ **健康信息學** | **批判性設計研究**

---

## 研究背景

### ChatGPT Health 與 Torch 收購案的啟示

2026 年 1 月，OpenAI 宣布推出 **ChatGPT Health**，允許用戶直接上傳健康記錄並獲得 AI 驅動的"個性化健康洞察"。同月收購 **Torch Health**，整合"統一醫療記憶系統"，深度融合 EHR 數據與對話式 AI。

**設計的雙面性：**
- **積極面：** 優秀的 UX 可以透明化數據流、支持知情決策
- **消極面：** 誤導性設計可能操縱用戶授權、淡化風險、限制數據控制權

---

## INFS 611 研究機會

### 核心研究問題（附文獻依據）

**主要問題：**

*現有文獻如何理解 AI 健康服務中的設計風險（暗黑模式）？這些知識如何指導未來的以用戶為中心的設計研究？*

**文獻依據：**
- 設計選擇並非中立——暗黑模式文獻提供了批判性分析工具[^1][^9][^10]

---

**子問題（適合 INFS 611 文獻綜述）：**

#### 1. 暗黑模式的用戶感知邊界研究

**問題：** 現有文獻如何識別用戶能察覺並反感的設計模式？這些證據如何幫助設計師或 AI 倫理實踐者在商業壓力下為倫理設計辯護？

**實踐困境：**
設計師並非不知道暗黑模式的存在，但在商業環境中，說服式設計仍需服務於商業目標。單純的倫理批判無法說服管理層。

**本研究的實踐價值：**
我們提供**基於用戶實證研究的輔助支持**：
1. 哪些設計模式會被用戶識別為操縱？→ 用戶感知的邊界
2. 哪些設計會損害長期信任與品牌形象？→ 商業風險論證
3. 如何在商業目標與用戶自主權之間找到平衡點？→ 替代設計策略

**主要文獻支持：**

**分類框架層（識別設計模式）：**
- Gray et al. (2018)[^1] 暗黑模式的基礎分類體系
- Brignull (2024)[^9] 擴展分類體系（90+ 種模式）
- **實踐價值：** 幫助設計師識別微妙的倫理邊界

**用戶感知層（證據基礎）：**
- Mathur et al. (2019)[^22] 大規模實證研究（11.1% 產品頁面使用暗黑模式）
- Luguri & Strahilevitz (2021)[^23] 用戶能識別並反感，導致品牌信任下降
- **實踐價值：** 商業論證：短期轉化 vs. 長期信任損失

**理論邊界層（倫理框架）：**
- Susser et al. (2019)[^10] 助推 vs. 操縱的概念邊界
- Acquisti et al. (2020) 倫理的助推設計範例
- **實踐價值：** 判斷設計是幫助用戶（助推）還是剝奪自主權（操縱）

**INFS 611 預期產出：**
1. 暗黑模式文獻綜述（10-15 篇），整理用戶感知與商業影響的既有研究
2. 初步概念框架草圖：用戶感知邊界、商業-倫理考量
3. 健康 AI 設計風險的文獻發現總結

**為 INFS 604/605 鋪路：**
- 界面評估：使用工具包評估 ChatGPT Health
- 用戶訪談：測試用戶是否能識別操縱性設計
- 設計建議：提供基於證據的替代方案

**關鍵轉變：** 從"批判暗黑模式"→"賦能設計師在商業現實中做出倫理選擇"

---

#### 2. 治理框架的設計轉譯問題

**問題：** WHO 與 NIST 的 AI 倫理原則如何轉化為具體的設計指南？現有文獻提供了哪些轉譯方法？

**理論依據：**
治理框架提供抽象原則，但設計師需要具體的界面設計策略。這是一個**知識轉譯**問題。

**主要文獻支持：**
- WHO (2021)[^7] 規範性框架，但缺乏設計操作指南
- NIST (2023)[^8] 風險管理流程，未具體到界面設計層級
- Amershi et al. (2019)[^2] 連接高層級原則與具體設計模式的範例（18條指南）
- Muller et al. (2020)[^18] HCI 社群的可信 AI 界面設計模式

**INFS 611 預期產出：**
- 治理框架文獻閱讀摘要（WHO, NIST 等主要框架）
- 初步映射表草圖：倫理原則與 HCI 設計建議的對應
- 文獻中發現的知識轉譯差距

**為 INFS 604/605 鋪路：**
該映射表將用於評估現實系統（如 ChatGPT Health）是否滿足倫理要求

---

#### 3. AI 素養與設計的交匯點

**問題：** 現有文獻如何理解 AI 素養的構成？設計如何支持或阻礙 AI 素養的發展？

**理論依據：**
AI 素養不僅是教育問題，也是設計問題。界面設計本身就在"教育"用戶理解 AI。

**主要文獻支持：**
- Long & Magerko (2020)[^21] AI 素養的五大能力領域
- Peixoto et al. (2025)[^14] XAI 的可訪問性差距
- Candello et al. (2020) AI 素養如何影響信任校準
- Wildenbos et al. (2018)[^13] MOLD-US 框架：數字健康可用性障礙

**INFS 611 預期產出：**
- AI 素養文獻閱讀摘要（8-12 篇）
- 文獻中提及的 AI 素養支持設計建議整理
- 初步概念框架草圖：連接 AI 素養與設計

**為 INFS 604/605 鋪路：**
該框架將指導用戶研究設計（訪談問題、可用性測試任務）

---

### 研究問題的整體邏輯

| 子問題 | 文獻領域 | 產出 | 可能應用 |
|--------|----------|------|----------------|
| 1. 暗黑模式邊界 | HCI、設計倫理 | 文獻發現整理 | 為未來界面分析提供參考 |
| 2. AI 素養與設計 | AI 教育、HCI | 概念框架草圖 | 為未來用戶研究提供思路 |

**核心貢獻：** 通過文獻閱讀**整理當前知識狀態**，為後續可能的實證研究提供文獻基礎。

---


## 文獻基礎

### 必讀核心文獻（8-10篇）

#### 暗黑模式與操縱性設計

1. **Gray, C. M., et al. (2018).** *The Dark Patterns of the UI (UX) of the Internet.*[^1]
   - 暗黑模式的分類與理論框架

2. **Susser, D., et al. (2019).** *Technology, autonomy, and manipulation.* Internet Policy Review.[^10]
   - 技術如何透過設計影響自主權

3. **Brignull, H. (2024).** *Deceptive Design: The Art of Manipulation.*[^9]
   - 實踐案例與設計模式目錄

#### 治理框架與負責任 AI

4. **WHO. (2021).** *Ethics and governance of artificial intelligence for health.*[^7]
   - 醫療 AI 的六大倫理原則

5. **NIST. (2023).** *AI Risk Management Framework.*[^8]
   - 結構化的 AI 風險管理方法

6. **Whitmire, E. et al. (2025).** *Foundation models in medicine are a social experiment.*[^6]
   - 批判性視角：醫學基礎模型的不確定性與倫理挑戰

#### AI 素養與用戶理解

7. **Long, D., & Magerko, B. (2020).** *What is AI Literacy?*[^21]
   - AI 素養的定義與核心能力框架

8. **Peixoto, M. J. P., et al. (2025).** *Who benefits from AI explanations?*[^14]
   - 當前 XAI 的可訪問性差距

#### HCI 與健康信息系統

9. **Ellis, J. R., et al. (2025).** *The halo effect.*[^3]
   - 對醫療機構的信任如何掩蓋第三方 AI 的隱私風險

10. **Amershi, S., et al. (2019).** *Guidelines for human-AI interaction.*[^2]
    - 18 條基於研究的 AI 交互設計指南

---



## 結語

本專案位於 **AI 倫理治理**、**批判性設計研究** 與 **HCI** 的交匯點。我們不僅要識別問題（暗黑模式、治理差距），更要提出解決方案（基於 AI 素養的設計原則）。


---

## 參考文獻

[^1]: Gray, C. M., Kou, Y., Battles, B., et al. (2018). *The dark patterns of the UI (UX) of the internet.* Proceedings of the 2018 IEEE Workshop on Ethics in Computer Security.

[^2]: Amershi, S., Bussone, A., Chandra, A., et2019). *Guidelines for human-AI interaction.* Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems, 1–13.

[^3]: Ellis, J. R., Dellavalle, N. S., et al. (2025). *The halo effect: Perceptions of information privacy among healthcare chatbot users.* Journal of the American Geriatrics Society, 73(2), 2341–2352.

[^6]: Whitmire, E., et al. (2025). *Foundation models in medicine are a social experiment.* Nature Digital Medicine. [in press]

[^7]: World Health Organization. (2021). *Ethics and governance of artificial intelligence for health.* WHO Guidelines. https://www.who.int/publications/i/item/9789240029200

[^8]: National Institute of Standards and Technology. (2023). *AI Risk Management Framework.* NIST. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

[^9]: Brignull, H. (2024). *Deceptive Design: The Art of Manipulation.* [Extended taxonomies]

[^10]: Susser, D., Roessler, B., & Nissenbaum, H. (2019). *Technology, autonomy, and manipulation.* Internet Policy Review, 8(2), 1–22.

[^12]: OpenAI. (January 2026). *Introducing ChatGPT Health.* https://openai.com/blog/introducing-chatgpt-health/ ; *AI as a Healthcare Ally* [White paper]

[^13]: Wildenbos, G. A., Peute, L., & Jaspers, M. (2018). *Aging barriers influencing mobile health usability for older adults: A literature-based framework (MOLD-US).* International Journal of Medical Informatics, 114, 66–75.

[^14]: Peixoto, M. J. P., et al. (2025). *Who benefits from AI explanations? Accessibility gaps in explainable AI for disabled users.* Proceedings of the IJCAI 2025 Workshop on Explainable AI.

[^18]: Muller, M. J., Angle, A., Chawla, P., et al. (2020). *Design patterns for trustworthy AI interfaces.* Proceedings of the 2020 ACM Designing Interactive Systems Conference.

[^21]: Long, D., & Magerko, B. (2020). *What is AI Literacy? Competencies and Design Considerations.* CHI 2020.

[^22]: Mathur, A., et al. (2019). *Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites.* CSCW 2019.

[^23]: Luguri, J., & Strahilevitz, L. (2021). *Shining a Light on Dark Patterns.* Journal of Legal Analysis, 13(1), 43–109.

### 額外資源

**個人觀察文章（非學術文獻）：**
- GAINSHIN. (2025). *作為父母，當 AI 對孩子暗示「依賴我吧」時，誰該為此負責？* AI 素養與隱私體驗. https://open.substack.com/pub/privacyux/p/ai-aff
- GAINSHIN. (2025). *Meta 演算法的沉默代價：失智老人赴約之死，以假亂真的AI謀算.* AI 素養與隱私體驗. https://open.substack.com/pub/privacyux/p/meta-ai

**新聞與產業報導：**
- BBC News. (8 January 2026). *OpenAI launches ChatGPT Health to review your medical records.*
- Time Magazine. (8 January 2026). *Is Giving ChatGPT Health Your Medical Records a Good Idea?*
- CNBC. (2025). *OpenAI says it plans ChatGPT changes after lawsuit blamed chatbot for teen's suicide.*
