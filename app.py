import streamlit as st
import os
from dotenv import load_dotenv
from agents.profiler import run_profiler
from agents.identifier import run_identifier
from agents.recommender import run_recommender

load_dotenv(override=True)

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="ET AI Concierge",
    page_icon="💼",
    layout="wide"
)

# ─── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #070b14;
    --surface: #0d1220;
    --surface2: #111827;
    --border: #1e2a3a;
    --border2: #253040;
    --accent: #ff6b35;
    --accent2: #ff9a6c;
    --text: #e0f0ff;
    --text2: #7a9aaa;
    --text3: #4a6a7a;
    --green: #1d9e75;
    --amber: #ba7517;
    --red: #e24b4a;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: var(--text2) !important;
    font-family: 'DM Sans', sans-serif !important;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text3) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Header ── */
.et-header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 18px 32px;
    position: relative;
    overflow: hidden;
}

.et-header::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,107,53,0.07) 0%, transparent 70%);
    pointer-events: none;
}

.et-badge {
    display: inline-block;
    background: rgba(255,107,53,0.1);
    border: 1px solid rgba(255,107,53,0.2);
    color: var(--accent);
    font-size: 10px;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.et-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
    margin: 0;
}

.et-title span { color: var(--accent); }

.et-sub {
    font-size: 12px;
    color: var(--text3);
    margin: 3px 0 0 0;
    font-weight: 300;
}

/* ── Chat messages ── */
.stChatMessage {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    margin: 6px 0 !important;
}

.stChatMessage p {
    color: var(--text2) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

/* ── Chat input padding fix ── */
.stChatInput textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding-left: 16px !important;
}

.stChatInput textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: none !important;
    outline: none !important;
}

.stChatInput > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

div[data-testid="stChatInput"] > div {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* ── Spinner inside chat ── */
div[data-testid="stSpinner"] {
    padding: 8px 0 !important;
}

div[data-testid="stSpinner"] p {
    color: var(--accent) !important;
    font-size: 13px !important;
}

/* ── Expander ── */
.stExpander {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.stExpander summary {
    color: var(--text3) !important;
    font-size: 12px !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

/* ── Scrollable containers ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: var(--bg) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]::-webkit-scrollbar {
    width: 4px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]::-webkit-scrollbar-thumb {
    background: var(--border2) !important;
    border-radius: 4px !important;
}

/* ── Agent status badges ── */
.agent-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
    border: 1px solid var(--border);
    background: var(--surface2);
}

.agent-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-done { background: #1d9e75; }
.dot-active { background: #ff6b35; animation: pulse 1.5s infinite; }
.dot-wait { background: #253040; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.agent-label { font-size: 12px; color: var(--text2); }
.agent-status-done { font-size: 10px; color: #1d9e75; margin-left: auto; }
.agent-status-active { font-size: 10px; color: #ff6b35; margin-left: auto; }
.agent-status-wait { font-size: 10px; color: var(--text3); margin-left: auto; }

/* ── Profile card ── */
.profile-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
}

.profile-row {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px solid var(--border);
    font-size: 12px;
}

.profile-row:last-child { border-bottom: none; }
.profile-key { color: var(--text3); }
.profile-val { color: var(--text2); font-weight: 500; }

/* ── Section title ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 12px;
}

/* ── Journey header ── */
.journey-header {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 0 0 12px 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
}

.journey-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}

.journey-sub { font-size: 12px; color: var(--text3); margin-top: 3px; }

/* ── Onboarding message ── */
.onboarding-msg {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 13px;
    color: var(--text2);
    line-height: 1.7;
    margin-bottom: 8px;
}

/* ── Score cards ── */
.score-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
}

.score-label {
    font-size: 10px;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.score-val {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--accent);
}

.score-val span { font-size: 11px; color: var(--text3); }
.score-insight { font-size: 10px; color: var(--text3); margin-top: 5px; line-height: 1.4; }

/* ── Score bar ── */
.score-bar-wrap { margin-top: 12px; margin-bottom: 8px; }
.score-bar-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--text3); margin-bottom: 6px; }
.score-bar-track { background: var(--border); border-radius: 4px; height: 5px; overflow: hidden; }
.score-bar-fill { height: 100%; background: linear-gradient(90deg, #ff6b35, #ff9a6c); border-radius: 4px; }

/* ── Gap card ── */
.gap-card {
    background: rgba(186,117,23,0.06);
    border: 1px solid rgba(186,117,23,0.18);
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    color: #ba7517;
    line-height: 1.6;
    margin-bottom: 8px;
}

.savings-tag {
    display: inline-block;
    background: rgba(29,158,117,0.1);
    border: 1px solid rgba(29,158,117,0.2);
    color: #1d9e75;
    font-size: 12px;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 20px;
    margin-top: 10px;
}

/* ── Need cards ── */
.need-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin-bottom: 8px;
}

.need-card.medium { border-left-color: var(--amber); }
.need-card.low { border-left-color: var(--green); }
.need-title { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 5px; }
.need-reason { font-size: 12px; color: var(--text2); line-height: 1.5; }
.need-impact { display: inline-block; background: rgba(29,158,117,0.08); border: 1px solid rgba(29,158,117,0.18); color: #1d9e75; font-size: 11px; padding: 3px 10px; border-radius: 20px; margin-top: 8px; }

/* ── Product cards ── */
.product-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}

.product-card:hover { border-color: var(--accent); }
.product-name { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: var(--accent); margin-bottom: 7px; }
.product-reason { font-size: 12px; color: var(--text2); line-height: 1.6; margin-bottom: 10px; }
.product-action { background: rgba(255,107,53,0.07); border: 1px solid rgba(255,107,53,0.15); border-radius: 7px; padding: 9px 12px; font-size: 12px; color: var(--accent); }
.product-action strong { font-weight: 500; color: var(--text3); display: block; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 3px; }

/* ── Audit ── */
.audit-item { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; }
.audit-agent { font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 600; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; }
.audit-action { font-size: 11px; color: var(--text3); margin-top: 2px; }

/* ── Waiting placeholder ── */
.waiting-box {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 40px 20px;
}

.waiting-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(255,107,53,0.08);
    border: 1px solid rgba(255,107,53,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.waiting-text {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--text3);
    text-align: center;
}

.waiting-sub {
    font-size: 12px;
    color: var(--text3);
    text-align: center;
    line-height: 1.6;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# ─── Initialize State ──────────────────────────────────────
def init_state():
    return {
        "name": None,
        "age": None,
        "occupation": None,
        "income_range": None,
        "investment_experience": None,
        "goals": [],
        "persona": None,
        "messages": [],
        "turn_count": 0,
        "profiling_complete": False,
        "identified_needs": None,
        "financial_scores": None,
        "overall_score": None,
        "monthly_savings_target": None,
        "gap_analysis": None,
        "financial_analysis": None,
        "recommended_products": None,
        "onboarding_path": None,
        "agent_log": [],
        "pipeline_complete": False,
        "identifier_complete": False,
        "processing": False,
    }

if "state" not in st.session_state:
    st.session_state.state = init_state()
    st.session_state.state["messages"].append({
        "role": "assistant",
        "content": "👋 Hi! I'm your ET AI Concierge. I'm here to help you discover everything Economic Times has to offer — from investing tools to financial planning.\n\nTo get started, could you tell me your name and what brings you to ET today?"
    })

state = st.session_state.state

# ─── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <p style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;
    color:#ff6b35;letter-spacing:-0.5px;margin-bottom:20px;">ET Concierge</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)

    def agent_html(label, state_key):
        if state_key == "done":
            return f'<div class="agent-item"><div class="agent-dot dot-done"></div><div class="agent-label">{label}</div><div class="agent-status-done">Done</div></div>'
        elif state_key == "active":
            return f'<div class="agent-item"><div class="agent-dot dot-active"></div><div class="agent-label">{label}</div><div class="agent-status-active">Active</div></div>'
        else:
            return f'<div class="agent-item"><div class="agent-dot dot-wait"></div><div class="agent-label">{label}</div><div class="agent-status-wait">Waiting</div></div>'

    a1 = "done" if state["profiling_complete"] else "active"
    a2 = "done" if state["identifier_complete"] else ("active" if state["profiling_complete"] else "wait")
    a3 = "done" if state["pipeline_complete"] else ("active" if state["identifier_complete"] else "wait")

    st.markdown(
        agent_html("Agent 1: Profiler", a1) +
        agent_html("Agent 2: Analyzer", a2) +
        agent_html("Agent 3: Recommender", a3),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if any([state["name"], state["age"], state["occupation"]]):
        st.markdown('<div class="section-label">User Profile</div>', unsafe_allow_html=True)
        rows = ""
        if state["name"]: rows += f'<div class="profile-row"><span class="profile-key">Name</span><span class="profile-val">{state["name"]}</span></div>'
        if state["age"]: rows += f'<div class="profile-row"><span class="profile-key">Age</span><span class="profile-val">{state["age"]}</span></div>'
        if state["occupation"]: rows += f'<div class="profile-row"><span class="profile-key">Occupation</span><span class="profile-val">{state["occupation"]}</span></div>'
        if state["investment_experience"]: rows += f'<div class="profile-row"><span class="profile-key">Experience</span><span class="profile-val">{state["investment_experience"]}</span></div>'
        if state["persona"]: rows += f'<div class="profile-row"><span class="profile-key">Persona</span><span class="profile-val">{state["persona"]}</span></div>'
        st.markdown(f'<div class="profile-card">{rows}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("↺ Start New Conversation"):
        st.session_state.state = init_state()
        st.session_state.state["messages"].append({
            "role": "assistant",
            "content": "👋 Hi! I'm your ET AI Concierge. I'm here to help you discover everything Economic Times has to offer.\n\nCould you tell me your name and what brings you to ET today?"
        })
        st.rerun()

# ─── Header ────────────────────────────────────────────────
st.markdown("""
<div class="et-header">
    <div class="et-badge">AI Concierge</div>
    <p class="et-title">ET <span>AI</span> Concierge</p>
    <p class="et-sub">Your intelligent guide to the Economic Times ecosystem</p>
</div>
""", unsafe_allow_html=True)

# ─── Two Column Layout — always shown ──────────────────────
chat_col, results_col = st.columns([1, 1])

# ─── CHAT COLUMN ───────────────────────────────────────────
with chat_col:
    # Fixed height scrollable chat box
    chat_container = st.container(height=560)
    with chat_container:
        # Show all messages
        for message in state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Show spinner INSIDE chat box while processing
        if state.get("processing"):
            with st.spinner("Thinking..."):
                state = run_profiler(state)
                state["processing"] = False
                st.session_state.state = state
            st.rerun()

    # Input box fixed below chat
    if not state["pipeline_complete"]:
        user_input = st.chat_input("Type your message here...")
        if user_input:
            state["messages"].append({"role": "user", "content": user_input})
            state["processing"] = True
            st.session_state.state = state
            st.rerun()

# ─── RESULTS COLUMN ────────────────────────────────────────
with results_col:
    results_container = st.container(height=560)
    with results_container:

        # Show waiting state before pipeline completes
        if not state["pipeline_complete"]:
            st.markdown("""
            <div class="waiting-box">
                <div class="waiting-icon">🤖</div>
                <div class="waiting-text">Your ET Journey Awaits</div>
                <div class="waiting-sub">
                    Complete the chat conversation on the left.<br>
                    Your personalized ET roadmap will appear here.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── Journey Header ──
            st.markdown("""
            <div class="journey-header">
                <p class="journey-title">Your Personalized ET Journey</p>
                <p class="journey-sub">Curated by 3 AI agents based on your financial profile</p>
            </div>
            """, unsafe_allow_html=True)

            # ── Onboarding Message ──
            if state.get("onboarding_path"):
                st.markdown(f'<div class="onboarding-msg">{state["onboarding_path"]}</div>', unsafe_allow_html=True)

            # ── Financial Health Score ──
            if state.get("overall_score"):
                st.markdown('<div class="section-label" style="margin-top:16px;">Financial Health Score</div>', unsafe_allow_html=True)
                scores = state.get("financial_scores", {})
                score = state["overall_score"]
                dims = [
                    ("emergency_preparedness", "Emergency"),
                    ("investment_readiness", "Investing"),
                    ("goal_clarity", "Goals"),
                    ("financial_awareness", "Awareness"),
                ]
                cols = st.columns(4)
                for col, (key, label) in zip(cols, dims):
                    with col:
                        s = scores.get(key, {}).get("score", 0)
                        insight = scores.get(key, {}).get("insight", "")[:55]
                        st.markdown(f"""
                        <div class="score-card">
                            <div class="score-label">{label}</div>
                            <div class="score-val">{s}<span>/10</span></div>
                            <div class="score-insight">{insight}...</div>
                        </div>
                        """, unsafe_allow_html=True)

                fill = int(score * 10)
                st.markdown(f"""
                <div class="score-bar-wrap">
                    <div class="score-bar-labels">
                        <span>Overall Financial Health</span>
                        <span style="color:#ff6b35;font-weight:600;">{score}/10</span>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill" style="width:{fill}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Gap Analysis ──
            if state.get("gap_analysis"):
                st.markdown('<div class="section-label" style="margin-top:16px;">Financial Gap Analysis</div>', unsafe_allow_html=True)
                savings = state.get("monthly_savings_target", "")
                savings_html = f'<div class="savings-tag">Recommended Savings: {savings}</div>' if savings else ""
                st.markdown(f"""
                <div class="gap-card">
                    {state["gap_analysis"]}
                    {savings_html}
                </div>
                """, unsafe_allow_html=True)

            # ── Financial Needs ──
            if state.get("identified_needs"):
                st.markdown('<div class="section-label" style="margin-top:16px;">Your Financial Needs</div>', unsafe_allow_html=True)
                for need in state["identified_needs"]:
                    if isinstance(need, dict):
                        priority = need.get("priority", "medium")
                        css_class = "need-card" if priority == "high" else ("need-card medium" if priority == "medium" else "need-card low")
                        title = need.get("need", "")
                        reason = need.get("reason", "")
                        impact = need.get("estimated_impact", "")
                        impact_html = f'<div class="need-impact">{impact}</div>' if impact else ""
                        st.markdown(f"""
                        <div class="{css_class}">
                            <div class="need-title">{title}</div>
                            <div class="need-reason">{reason}</div>
                            {impact_html}
                        </div>
                        """, unsafe_allow_html=True)

            # ── Product Recommendations ──
            if state.get("recommended_products"):
                st.markdown('<div class="section-label" style="margin-top:16px;">Recommended ET Products</div>', unsafe_allow_html=True)
                for product in state["recommended_products"]:
                    if isinstance(product, dict):
                        name = product.get("product", "")
                        reason = product.get("reason", "")
                        action = product.get("action", "")
                        st.markdown(f"""
                        <div class="product-card">
                            <div class="product-name">{name}</div>
                            <div class="product-reason">{reason}</div>
                            <div class="product-action">
                                <strong>Next Step</strong>
                                {action}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            # ── Audit Trail ──
            with st.expander("View Agent Decision Trail"):
                if state.get("agent_log"):
                    for log in state["agent_log"]:
                        if isinstance(log, dict):
                            agent = log.get("agent", "")
                            action = log.get("action", "")
                            st.markdown(f"""
                            <div class="audit-item">
                                <div class="audit-agent">{agent}</div>
                                <div class="audit-action">{action}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if "output" in log:
                                output = log["output"]
                                if isinstance(output, (dict, list)):
                                    st.json(output)
                                else:
                                    st.write(output)

# ─── Agent 2 Auto-run ───────────────────────────────────────
if state["profiling_complete"] and not state["identifier_complete"] and not state["pipeline_complete"]:
    with chat_col:
        with st.spinner("🔍 Agent 2: Analysing your financial profile..."):
            state = run_identifier(state)
            state["identifier_complete"] = True
    st.session_state.state = state
    st.rerun()

# ─── Agent 3 Auto-run ───────────────────────────────────────
if state["identifier_complete"] and not state["pipeline_complete"]:
    with chat_col:
        with st.spinner("📦 Agent 3: Finding best ET products for you..."):
            state = run_recommender(state)
            state["pipeline_complete"] = True
    st.session_state.state = state
    st.rerun()