# 🏗️ ET AI Concierge — Architecture Document

**Hackathon:** ET AI Hackathon 2026
**Track:** 7 — AI Concierge for ET
**Builder:** Tanish Gupta

---

## 📐 System Overview

ET AI Concierge is a multi-agent AI system that autonomously
completes a full user journey:

```
User Input → Agent 1 (Profiler) → Agent 2 (Analyzer) → Agent 3 (Recommender) → Personalized Output
```

---

## 🤖 Agent Roles & Responsibilities

### Agent 1 — Profiler

| Property  | Detail                                                                              |
| --------- | ----------------------------------------------------------------------------------- |
| Role      | Conversational user profiling                                                       |
| Input     | Raw user messages                                                                   |
| Output    | Structured user profile (name, age, occupation, income, experience, goals, persona) |
| Max Turns | 3 conversational turns                                                              |
| Trigger   | Activated on every user message until profile complete                              |
| Handoff   | Triggers Agent 2 automatically when [PROFILE_COMPLETE] detected                     |

### Agent 2 — Financial Analyzer

| Property   | Detail                                                                          |
| ---------- | ------------------------------------------------------------------------------- |
| Role       | Deep financial health assessment                                                |
| Input      | Structured user profile from Agent 1                                            |
| Output     | Financial scores, gap analysis, savings target, prioritized needs               |
| Dimensions | Emergency preparedness, Investment readiness, Goal clarity, Financial awareness |
| Handoff    | Passes enriched analysis to Agent 3                                             |

### Agent 3 — Recommender

| Property     | Detail                                                        |
| ------------ | ------------------------------------------------------------- |
| Role         | ET product matching and onboarding                            |
| Input        | Financial analysis from Agent 2 + ET product catalog          |
| Output       | 2-3 personalized product recommendations + onboarding message |
| Logic        | Matches needs to products, adapts tone per persona            |
| Final Output | Personalized ET journey with specific next steps              |

---

## 🔄 Agent Communication Flow

```
┌─────────────────────────────────────────────────────┐
│                    USER INPUT                        │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              AGENT 1: PROFILER                       │
│  • Conversational extraction                         │
│  • Persona detection                                 │
│  • Profile structuring                               │
│  • Max 3 turns                                       │
└─────────────────────┬───────────────────────────────┘
                      │ profile_complete = True
                      ▼
┌─────────────────────────────────────────────────────┐
│           AGENT 2: FINANCIAL ANALYZER                │
│  • 4-dimension scoring (0-10)                        │
│  • Gap analysis with savings target                  │
│  • Top 3 needs identification                        │
│  • Priority ranking                                  │
└─────────────────────┬───────────────────────────────┘
                      │ identifier_complete = True
                      ▼
┌─────────────────────────────────────────────────────┐
│           AGENT 3: RECOMMENDER                       │
│  • ET product catalog matching                       │
│  • Persona-aware recommendations                     │
│  • Personalized onboarding message                   │
│  • Specific next steps per product                   │
└─────────────────────┬───────────────────────────────┘
                      │ pipeline_complete = True
                      ▼
┌─────────────────────────────────────────────────────┐
│              PERSONALIZED OUTPUT                     │
│  • Financial health scores                           │
│  • Gap analysis                                      │
│  • Prioritized needs                                 │
│  • ET product recommendations                        │
│  • Onboarding path                                   │
│  • Full audit trail                                  │
└─────────────────────────────────────────────────────┘
```

---

## 🗂️ Shared State Schema

All agents communicate through a shared state dictionary:

```python
{
  # User Profile (populated by Agent 1)
  "name": str,
  "age": int,
  "occupation": str,
  "income_range": str,
  "investment_experience": str,  # beginner/intermediate/expert
  "goals": list,
  "persona": str,  # new_user/lapsed_user/active_user

  # Financial Analysis (populated by Agent 2)
  "financial_scores": dict,    # 4 dimension scores
  "overall_score": int,        # 0-10
  "monthly_savings_target": str,
  "gap_analysis": str,
  "identified_needs": list,    # top 3 needs

  # Recommendations (populated by Agent 3)
  "recommended_products": list,
  "onboarding_path": str,

  # Pipeline Control
  "profiling_complete": bool,
  "identifier_complete": bool,
  "pipeline_complete": bool,

  # Audit Trail
  "agent_log": list  # every agent decision logged
}
```

---

## 🛠️ Tool Integrations

| Tool                    | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| Google Gemini 2.5 Flash | LLM for all 3 agents                        |
| Streamlit               | Frontend UI and session state               |
| python-dotenv           | Secure API key management                   |
| ET Product Catalog      | Internal knowledge base for recommendations |

---

## ⚠️ Error Handling

| Scenario                         | Handling                                    |
| -------------------------------- | ------------------------------------------- |
| LLM returns invalid JSON         | Try/catch with fallback defaults            |
| API key missing                  | Clear error message with setup instructions |
| Profile incomplete after 3 turns | Proceeds with available data                |
| Unknown persona detected         | Defaults to new_user flow                   |
| Product catalog mismatch         | Falls back to ET Money as safe default      |

---

## 🔒 Compliance & Guardrails

- No competitor platforms mentioned in recommendations
- Non-intrusive cross-sell (penalized if pushy per judging criteria)
- All recommendations include specific next steps
- Full audit trail of every agent decision
- No financial advice given — only ET product guidance

---

## 📊 Autonomy Depth

| Step                        | Human Involved?    |
| --------------------------- | ------------------ |
| 1. User sends first message | ✅ Human types     |
| 2. Profile extraction       | ❌ Fully automated |
| 3. Persona detection        | ❌ Fully automated |
| 4. Financial scoring        | ❌ Fully automated |
| 5. Gap analysis             | ❌ Fully automated |
| 6. Needs identification     | ❌ Fully automated |
| 7. Product matching         | ❌ Fully automated |
| 8. Onboarding message       | ❌ Fully automated |

**7 out of 8 steps are fully autonomous.**

---

## 💰 Impact Model

| Metric                       | Assumption        | Impact             |
| ---------------------------- | ----------------- | ------------------ |
| ET has 50M+ registered users | 10% use concierge | 5M users profiled  |
| Average ET product discovery | 10% → 60%         | 5x improvement     |
| Manual onboarding cost       | ₹50/user          | ₹25 crore saved    |
| Cross-sell conversion        | 2% → 8%           | 4x revenue uplift  |
| Onboarding time              | 20 mins → 3 mins  | 85% time reduction |
