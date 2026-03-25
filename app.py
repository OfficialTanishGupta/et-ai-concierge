import streamlit as st
import os
from dotenv import load_dotenv
from agents.profiler import run_profiler
from agents.identifier import run_identifier
from agents.recommender import run_recommender

load_dotenv(override=True)

# Page Config
st.set_page_config(
    page_title="ET AI Concierge",
    page_icon="💼",
    layout="centered"
)

# Custom CSS 
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .header-title { color: #ff6b35; font-size: 28px; font-weight: bold; }
    .subheader { color: #666; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# Header 
st.markdown('<p class="header-title">💼 ET AI Concierge</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Your personal guide to everything Economic Times offers</p>', unsafe_allow_html=True)
st.divider()

# Initialize State 
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
        "recommended_products": None,
        "onboarding_path": None,
        "agent_log": [],
        "pipeline_complete": False,
        "identifier_complete": False,
    }

if "state" not in st.session_state:
    st.session_state.state = init_state()
    st.session_state.state["messages"].append({
        "role": "assistant",
        "content": "👋 Hi! I'm your ET AI Concierge. I'm here to help you discover everything Economic Times has to offer — from investing tools to financial planning.\n\nTo get started, could you tell me your name and what brings you to ET today?"
    })

state = st.session_state.state

# Sidebar 
with st.sidebar:
    st.markdown("### 🤖 Agent Pipeline Status")

    # Agent 1
    if state["profiling_complete"]:
        st.success("✅ Agent 1: Profiler — Done")
    else:
        st.warning("⏳ Agent 1: Profiler — Active")

    # Agent 2
    if state["identifier_complete"]:
        st.success("✅ Agent 2: Identifier — Done")
    elif state["profiling_complete"] and not state["identifier_complete"]:
        st.warning("⏳ Agent 2: Identifier — Active")
    else:
        st.info("⏸️ Agent 2: Identifier — Waiting")

    # Agent 3
    if state["pipeline_complete"]:
        st.success("✅ Agent 3: Recommender — Done")
    elif state["identifier_complete"] and not state["pipeline_complete"]:
        st.warning("⏳ Agent 3: Recommender — Active")
    else:
        st.info("⏸️ Agent 3: Recommender — Waiting")

    st.divider()

    # User profile
    if any([state["name"], state["age"], state["occupation"]]):
        st.markdown("### 👤 User Profile")
        if state["name"]:
            st.write(f"**Name:** {state['name']}")
        if state["age"]:
            st.write(f"**Age:** {state['age']}")
        if state["occupation"]:
            st.write(f"**Occupation:** {state['occupation']}")
        if state["investment_experience"]:
            st.write(f"**Experience:** {state['investment_experience']}")
        if state["persona"]:
            st.write(f"**Persona:** {state['persona']}")

    st.divider()

    if st.button("🔄 Start New Conversation"):
        st.session_state.state = init_state()
        st.session_state.state["messages"].append({
            "role": "assistant",
            "content": "👋 Hi! I'm your ET AI Concierge. I'm here to help you discover everything Economic Times has to offer.\n\nCould you tell me your name and what brings you to ET today?"
        })
        st.rerun()

# Chat Messages 
for message in state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Results Panel 
if state["pipeline_complete"]:
    st.divider()
    st.markdown("## 🎯 Your Personalized ET Journey")

    # Onboarding message
    if state["onboarding_path"]:
        st.info(state["onboarding_path"])

    # Identified needs
    # Financial Health Score
    if state.get("overall_score"):
        st.markdown("### 📊 Your Financial Health Score")
        score = state["overall_score"]
        col1, col2, col3, col4 = st.columns(4)

        scores = state.get("financial_scores", {})

        with col1:
            s = scores.get("emergency_preparedness", {}).get("score", 0)
            st.metric("🛡️ Emergency", f"{s}/10")
            st.caption(scores.get("emergency_preparedness", {}).get("insight", ""))

        with col2:
            s = scores.get("investment_readiness", {}).get("score", 0)
            st.metric("📈 Investing", f"{s}/10")
            st.caption(scores.get("investment_readiness", {}).get("insight", ""))

        with col3:
            s = scores.get("goal_clarity", {}).get("score", 0)
            st.metric("🎯 Goals", f"{s}/10")
            st.caption(scores.get("goal_clarity", {}).get("insight", ""))

        with col4:
            s = scores.get("financial_awareness", {}).get("score", 0)
            st.metric("🧠 Awareness", f"{s}/10")
            st.caption(scores.get("financial_awareness", {}).get("insight", ""))

        st.progress(score / 10)
        st.caption(f"Overall Financial Health: {score}/10")

    # Gap Analysis
    if state.get("gap_analysis"):
        st.markdown("### 🔎 Financial Gap Analysis")
        st.warning(state["gap_analysis"])
        if state.get("monthly_savings_target"):
            st.info(f"💰 Recommended Monthly Savings Target: **{state['monthly_savings_target']}**")

    # Identified needs
    if state["identified_needs"]:
        st.markdown("### 🔍 Your Financial Needs")
        for need in state["identified_needs"]:
            if isinstance(need, dict):
                priority = need.get("priority", "medium")
                priority_color = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                need_title = need.get("need", "")
                need_reason = need.get("reason", "")
                estimated_impact = need.get("estimated_impact", "")
                with st.container(border=True):
                    st.markdown(f"{priority_color} **{need_title}**")
                    st.write(need_reason)
                    if estimated_impact:
                        st.success(f"✨ Impact: {estimated_impact}")
    else:
        st.warning("No needs identified yet")

    # Product recommendations
    if state["recommended_products"]:
        st.markdown("### 📦 Recommended ET Products")
        for product in state["recommended_products"]:
            if isinstance(product, dict):
                product_name = product.get("product", "")
                product_reason = product.get("reason", "")
                product_action = product.get("action", "")
                with st.container(border=True):
                    st.markdown(f"🏷️ **{product_name}**")
                    st.write(f"💡 {product_reason}")
                    st.success(f"👉 Next Step: {product_action}")
    else:
        st.warning("No products recommended yet")

    # Audit trail
    with st.expander("🔍 View Agent Decision Trail"):
        if state["agent_log"]:
            for log in state["agent_log"]:
                if isinstance(log, dict):
                    agent = log.get("agent", "Unknown")
                    action = log.get("action", "")
                    with st.container(border=True):
                        st.markdown(f"**🤖 {agent}** → {action}")
                        if "output" in log:
                            output = log["output"]
                            if isinstance(output, (dict, list)):
                                st.json(output)
                            else:
                                st.write(output)
                        if "error" in log:
                            st.error(f"Error: {log['error']}")
        else:
            st.write("No agent logs yet")

# Chat Input 
if not state["pipeline_complete"]:
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message
        state["messages"].append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Agent 1: Profiler 
        with st.chat_message("assistant"):
            with st.spinner("🧠 Agent 1: Understanding your profile..."):
                state = run_profiler(state)
                latest_response = state["messages"][-1]["content"]
                st.markdown(latest_response)

        st.session_state.state = state
        st.rerun()

# Auto-run Agents 2 & 3 after profiling 
if state["profiling_complete"] and not state["identifier_complete"] and not state["pipeline_complete"]:

    #  Agent 2: Identifier
    with st.spinner("🔍 Agent 2: Identifying your financial needs..."):
        state = run_identifier(state)
        state["identifier_complete"] = True

    st.session_state.state = state
    st.rerun()

if state["identifier_complete"] and not state["pipeline_complete"]:

    # Agent 3: Recommender
    with st.spinner("📦 Agent 3: Finding best ET products for you..."):
        state = run_recommender(state)
        state["pipeline_complete"] = True

    st.session_state.state = state
    st.rerun()