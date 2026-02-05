# Framework Map V2 Design Plan

Based on the **Week 4 Pivot Report**, the conceptual map needs to shift from a "Static Dark Pattern" model to a "Dynamic Agentic Risk" model.

## Core Shift Summary

| Element | Version 1 (Static) | Version 2 (Dynamic/Agentic) |
| :--- | :--- | :--- |
| **Theme 1 (User)** | General Vulnerability (Cognitive decline, etc.) | **The Halo Effect** (High Trust = Low Defense)<br>*(Focus on "Trust Transfer" from Health brands)* |
| **Theme 2 (Risk)** | Static Dark Patterns (Gray 2018)<br>Taxonomy of 5 types | **Hypernudging & Hidden Influence** (Duane 2025)<br>*(Dynamic, data-driven, real-time tailoring)* |
| **Theme 3 (System)** | General HCI & Chatbots | **Agentic AI Capabilities**<br>*(Autonomy, Memory, Semantic Commit)* |
| **Theme 4 (Gov)** | General Principles (WHO/NIST) | **The "Audit Gap"**<br>*(Principles exist but designers lack tools to test them in dynamic systems)* |
| **Outcome** | "Design Interventions" (General) | **Heuristic Evaluation / Audit Tool**<br>*(Specific method for pre-deployment testing)* |

---

## Proposed Mermaid Structure (Graph TD)

### 1. Context Layer (Top)
*   **Node A (User):** older adults **Trusting** the System (Halo Effect).
    *   *Key Concept:* "I trust this medical brand, so I trust its AI agent."
*   **Node B (System):** Agentic AI **Observing** the User.
    *   *Key Concept:* Long-term memory, Real-time adaptation.

### 2. Interaction Layer (Middle - The "risk mechanism")
*   **Node C (The Mechanism):** **Hypernudging** (Duane et al., 2025).
    *   *Process:* The AI uses *Node B* (Data) to exploit *Node A* (Trust) via subtle, personalized UI changes.
    *   *Definition:* "Hidden Influence" (Susser).

### 3. The Problem Layer (Why it continues)
*   **Node D (The Gap):** **Invisibility**.
    *   Governance principles (WHO/NIST) fail because these risks are *dynamic* and *invisible* in static mockups.

### 4. The Solution Layer (Bottom)
*   **Node E (Contribution):** **Heuristic Audit Tool**.
    *   *Goal:* Make the invisible visible.
    *   *Method:* "Test for seams," "Check for contestability."

---

## Implementation Details

I will use `mermaid` with `graph TD` (Top-Down).

*   **Styles**:
    *   **User/Context**: Blue/Neutral.
    *   **Risk Mechanism (Hypernudge)**: Red/Warning (to highlight the pivot focus).
    *   **Solution**: Green (Actionable Tool).

### Draft Mermaid Code Structure
```mermaid
graph TD
    %% Themes
    User[Theme 1: User Context<br><b>The Halo Effect</b><br>(High Trust in Health Brand)]
    System[Theme 3: System Context<br><b>Agentic AI</b><br>(Memory + Autonomy)]
    
    %% The Dynamic Risk
    Risk[Theme 2: Dynamic Risk<br><b>Hypernudging</b><br>(Duane 2025)<br><i>Real-time, Personalized Manipulation</i>]
    
    %% The Governance Gap
    Gov[Theme 4: Governance Gap<br><b>Principles vs. Practice</b><br>Static guidelines cannot catch<br>dynamic risks]
    
    %% Output
    Tool[<b>OUTPUT: Heuristic Audit Tool</b><br><i>"Test for Breakdown"</i><br>(Zubatiy 2023)]

    %% Connections
    User -->|Trusts| Risk
    System -->|Enables| Risk
    Risk -->|Violates| Gov
    Gov -->|Requires| Tool
    
    %% Styling
    classDef user fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef risk fill:#FFEBEE,stroke:#C62828,stroke-width:2px;
    classDef gov fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef tool fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    
    class User,System user;
    class Risk risk;
    class Gov gov;
    class Tool tool;
```
