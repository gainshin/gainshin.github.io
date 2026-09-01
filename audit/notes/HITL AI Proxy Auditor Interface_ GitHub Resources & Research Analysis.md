# HITL AI Proxy Auditor Interface: GitHub Resources & Research Analysis

# 摘要

V5 研究問題 (RQ) 的三個核心目標：

1. 呈現真實的風險查核證據 (Surfacing Real Risk-Check Evidence)
確立評估的黃金標準：InvisibleBench 被標示為與 RQ 最相關的資源，它作為照護 AI 的「部署閘門 (deployment gate)」，提供了一套「守門與品質 (Gate + Quality)」的評分架構。它具體測試了危機偵測、法規遵循以及長期照護中的情緒穩定性，這直接定義了在「機構健康 AI」中，系統必須向使用者呈現哪些具體的「風險查核」結果。

介面呈現策略：在實作上，文件建議參考「顧問型 AI 控制台 (Advisory AI Console)」的工作流程，在介面上使用「政策裁定徽章 (policy verdict badges)」與「理由摘要 (justification summaries)」來視覺化這些查核證據。

機構級別的技術支援：VerifyWise 是一個 AI 治理平台，它可以用來支援 V5 框架中提到的「機構審查員 (institutional reviewer)」角色，確保機構端有工具能產出這些證據。

2. 校準信任 (Calibrating Trust)
預防「充滿自信的錯誤」：Trust-Intervention 專案的研究指出，使用者的「信任修復 (trust recovery)」過程是非常緩慢的。因此，代理稽核員在設計上必須極力避免 AI 產出「充滿自信的錯誤 (confidently incorrect)」，以免發生不可逆的信任崩盤。

不確定性的視覺化：在初始的「擷取 (Capture)」階段，系統可以利用信心度呈現 (Confidence Presentation) 技術，向代理人（如照護者或醫師）明確傳達 AI 內部的不確定性。

UX 設計模式：aiuxdesign.guide 提供了專門針對信任校準的 UI/UX 模式，強調必須讓使用者的認知與系統實際的可靠性保持一致。同時，End-User XAI 的分析有助於理解不同的解釋目標（例如是為了校準信任，還是為了偵測偏見）會如何影響終端使用者。

3. 減少照護者負擔 (Reducing Caregiver Burden via Capture & Replay)
架構標準化的 HITL 通訊：HITL Protocol 提供了一個類似 OAuth 的開放標準，用來無縫串接服務、AI Agent 與人類。配合 LuaN1aoAgent（支援專家監督與介入的認知驅動 AI Agent），這為構建流暢的「呼叫人類代理」流程提供了底層結構。

實踐「擷取與重播」的邏輯：要真正減少照護者的重複勞動，系統必須重播先前高品質審查的「邏輯 (logic)」，而不僅僅是重複動作。Governor 專案提供了「狀態擷取與重播 (State Capture and Replay)」功能以供稽核；PI Agent Rust 定義了高效能的擷取與重播情境；而 Human Replay 雖然是針對輸入節奏的 JS 函式庫，但其概念可以轉化為記錄照護者是「如何」一步步進行風險審查的。

制度面的負擔轉移：V5 框架將代理角色擴展至醫師和機構，配合上述的工具（如 VerifyWise），能實質將把關的重擔從單一家庭照護者身上分散出去。

## 1. Core Frameworks & Benchmarks (HITL & Caregiving AI)

| Project Name           | GitHub Link                                                                   | Key Features & Relevance to RQ                                                                                                                                                                                                                                                                    |
| :--------------------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **InvisibleBench**     | [givecareapp/givecare-bench](https://github.com/givecareapp/givecare-bench)   | **The most relevant resource.** A deployment gate for caregiving AI. Features a "Gate + Quality" scoring architecture, testing crisis detection, regulatory compliance, and emotional stability in long-term caregiving. Directly addresses "institutional health AI" and "risk-check" scenarios. |
| **HITL Protocol**      | [rotorstar/hitl-protocol](https://github.com/rotorstar/hitl-protocol)         | An open standard for human-in-the-loop interactions. Connects services, agents, and humans, similar to how OAuth handles authentication. Useful for structuring the "Proxy Auditor" communication.                                                                                                |
| **Trust Intervention** | [zouharvi/trust-intervention](https://github.com/zouharvi/trust-intervention) | Focuses on **Trust Calibration**. Studies how user trust evolves under uncertainty and miscalibration (confidently incorrect vs. unconfidently correct). Provides a UI for testing trust-eroding events.                                                                                          |
| **LuaN1aoAgent**       | [SanMuzZzZz/LuaN1aoAgent](https://github.com/SanMuzZzZz/LuaN1aoAgent)         | A cognitive-driven AI agent supporting HITL mode for expert supervision and intervention in decision-making processes.                                                                                                                                                                            |

## 2. Capture & Replay Mechanisms

| Project Name      | GitHub Link                                                                           | Relevance to "Capture & Replay Human Support"                                                                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PI Agent Rust** | [Dicklesworthstone/pi_agent_rust](https://github.com/Dicklesworthstone/pi_agent_rust) | Explicitly defines "extension capture and replay scenarios." High-performance agent framework that could serve as a technical base for recording human support logic.                      |
| **Governor**      | [LyzrCore/governor](https://github.com/LyzrCore/governor)                             | Features "State Capture and Replay." Designed for governing AI agents by capturing their state and allowing for replaying/auditing, which aligns with the "Proxy Auditor" goal.            |
| **Human Replay**  | [einenlum/human-replay](https://github.com/einenlum/human-replay)                     | A JS library for recording and replaying human user input (rhythm, pauses, corrections). While focused on typing, the concept is applicable to capturing "how" a caregiver reviews a risk. |

## 3. Trust Calibration & Evidence Surfacing

| Resource / Tool           | Source / Link                                                               | Key Insights for V5 Framework                                                                                             |
| :------------------------ | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **AI UX Design Patterns** | [aiuxdesign.guide](https://www.aiuxdesign.guide/patterns/trust-calibration) | Provides patterns for **Trust Calibration**, emphasizing alignment between user perception and actual system reliability. |
| **End-User XAI**          | [weinajin/end-user-xai](https://github.com/weinajin/end-user-xai)           | Provides analysis on how different explanation goals (e.g., trust calibration, bias detection) affect end-users.          |
| **VerifyWise**            | [verifywise-ai/verifywise](https://github.com/verifywise-ai/verifywise)     | An AI governance platform for safe and responsible AI use, relevant for the "institutional reviewer" role in V5.          |

## 4. Technical Implementation Notes for RQ (V5)

### Surfacing Real Risk-Check Evidence
- **InvisibleBench**'s gate-based scoring provides a model for what "evidence" looks like: pass/fail criteria on specific safety dimensions (Safety, Compliance, Regard, Coordination).
- **Evidence Surfacing Patterns**: Found in "Advisory AI Console" workflows, suggesting the use of policy verdict badges and justification summaries.

### Calibrating Trust
- **Trust-Intervention**'s research shows that trust recovery is slow; therefore, the Proxy Auditor must prioritize preventing "confidently incorrect" outputs.
- Use **Confidence Presentation** (as seen in EMNLP 2023 papers) to signal uncertainty to the Proxy (Caregiver/Physician) during the initial "Capture" phase.

### Reducing Caregiver Burden
- **Capture & Replay**: By replaying the "logic" (not just the action) of a previous high-quality review, the system reduces the need for repeated manual checks.
- **Institutional Delegation**: V5's expansion to include physicians and institutional reviewers (supported by tools like **VerifyWise**) shifts some burden away from family caregivers.
