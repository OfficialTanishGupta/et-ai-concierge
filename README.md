# 💼 ET AI Concierge

> AI-powered personal guide to the Economic Times ecosystem

Built for **ET AI Hackathon 2026** | Track 7: AI Concierge for ET

---

## 🎯 Problem

Most ET users discover only 10% of what ET offers. There is no
intelligent guide that understands who you are and maps you to
the right ET products, tools and services.

## 💡 Solution

A multi-agent AI concierge that profiles users in under 3
conversational turns and autonomously delivers a personalized
ET journey — from need identification to product recommendation.

---

## 🤖 Agent Architecture

### Agent 1 — Profiler

- Extracts user profile in maximum 3 conversational turns
- Identifies persona: new_user, lapsed_user, active_user
- Triggers Agents 2 and 3 automatically on completion

### Agent 2 — Financial Analyzer

- Scores user across 4 financial dimensions (0-10)
- Performs gap analysis with monthly savings target
- Identifies top 3 prioritized financial needs

### Agent 3 — Recommender

- Maps identified needs to ET product catalog
- Generates personalized onboarding message
- Creates specific next steps for each recommendation

---

## 🧪 Mandatory Scenarios Handled

### Scenario 1 — Cold Start New User

> 28-year-old first-time investor, never invested before

- Agent profiles in 2-3 turns
- Recommends ET Money + ET Masterclass
- Simple language, no jargon

### Scenario 2 — Lapsed ET Prime Subscriber

> User who left 90 days ago, heavy markets content consumer

- Detects lapsed_user persona
- Surfaces new value added since lapse
- Re-engagement focused recommendations

### Scenario 3 — Cross-Sell Moment

> Active ET Markets reader searching for home loan rates

- Detects home purchase intent signal
- Pivots to ET Financial Services
- Non-intrusive, contextual recommendation

---

## 🛠️ Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| Frontend         | Streamlit                   |
| Agent Framework  | Custom multi-agent pipeline |
| LLM              | Google Gemini 2.5 Flash     |
| Language         | Python 3.x                  |
| State Management | Session-based state dict    |

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key (free tier)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/OfficialTanishGupta/et-ai-concierge.git
cd et-ai-concierge

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free API key at: https://aistudio.google.com

### Run the App

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 📊 Impact Model

| Metric                | Current      | With ET AI Concierge |
| --------------------- | ------------ | -------------------- |
| ET Product Discovery  | 10%          | 60%+                 |
| Onboarding Time       | 15-20 mins   | Under 3 mins         |
| Cross-sell Conversion | Manual       | Automated            |
| User Profiling Cost   | High (human) | Near zero (AI)       |

---

## 🗂️ Project Structure

```
et-ai-concierge/
├── agents/
│   ├── profiler.py       # Agent 1: User profiling
│   ├── identifier.py     # Agent 2: Financial analysis
│   └── recommender.py    # Agent 3: Product recommendation
├── utils/
│   ├── state.py          # Shared state schema
│   └── et_products.py    # ET product catalog
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 👤 Author

**Tanish Gupta**
ET AI Hackathon 2026 — Track 7: AI Concierge for ET
