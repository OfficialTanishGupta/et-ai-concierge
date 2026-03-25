import streamlit as st
import os
from dotenv import load_dotenv
from agents.profiler import run_profiler
from agents.identifier import run_identifier
from agents.recommender import run_recommender

load_dotenv()
st.set_page_config(
    page_title="ET AI Concierge",
    page_icon="💼",
    layout="centered"
)
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; margin: 8px 0; }
    .product-card {
        background: white;
        border-left: 4px solid #ff6b35;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .need-card {
        background: white;
        border-left: 4px solid #1a73e8;
        border-radius: 8px;
        padding: 12px;
        margin: 6px 0;
    }
    .profile-card {
        background: #e8f4fd;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    .audit-card {
        background: #f0f0f0;
        border-radius: 8px;
        padding: 12px;
        margin: 6px 0;
        font-size: 12px;
    }
    .header-title {
        color: #ff6b35;
        font-size: 28px;
        font-weight: bold;
    }
    .subheader {
        color: #666;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header-title">💼 ET AI Concierge</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Your personal guide to everything Economic Times offers</p>', unsafe_allow_html=True)
st.divider()

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
        "pipeline_complete": False
    }

if "state" not in st.session_state:
    st.session_state.state = init_state()
    # Adding welcome message
    st.session_state.state["messages"].append({
        "role": "assistant",
        "content": "👋 Hi! I'm your ET AI Concierge. I'm here to help you discover everything Economic Times has to offer — from investing tools to financial planning.\n\nTo get started, could you tell me your name and what brings you to ET today?"
    })

state = st.session_state.state

with st.sidebar:
    st.markdown("### 🤖 Agent Pipeline")
    
    # Agent 1 status
    if state["profiling_complete"]:
        st.success("✅ Agent 1: Profiler")
    else:
        st.warning("⏳ Agent 1: Profiler (active)")
    
    # Agent 2 status
    if state["identified_needs"]:
        st.success("✅ Agent 2: Identifier")
    else:
        st.info("⏸️ Agent 2: Identifier (waiting)")
    
    # Agent 3 status
    if state["recommended_products"]:
        st.success("✅ Agent 3: Recommender")
    else:
        st.info("⏸️ Agent 3: Recommender (waiting)")

    st.divider()

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

for message in state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if state["pipeline_complete"]:

    st.divider()
    st.markdown("## 🎯 Your Personalized ET Journey")

    if state["onboarding_path"]:
        st.info(state["onboarding_path"])

    if state["identified_needs"]:
        st.markdown("### 🔍 Your Financial Needs")
        for need in state["identified_needs"]:
            priority_color = "🔴" if need["priority"] == "high" else "🟡" if need["priority"] == "medium" else "🟢"
            st.markdown(f"""
            <div class="need-card">
                <b>{priority_color} {need['need']}</b><br>
                <small>{need['reason']}</small>
            </div>
            """, unsafe_allow_html=True)

    if state["recommended_products"]:
        st.markdown("### 📦 Recommended ET Products")
        for product in state["recommended_products"]:
            st.markdown(f"""
            <div class="product-card">
                <b>🏷️ {product['product']}</b><br>
                <small>💡 {product['reason']}</small><br><br>
                <b>👉 Next Step:</b> {product['action']}
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🔍 View Agent Decision Trail"):
        for log in state["agent_log"]:
            st.markdown(f"""
            <div class="audit-card">
                <b>🤖 {log['agent']}</b> → {log['action']}
            </div>
            """, unsafe_allow_html=True)

if not state["pipeline_complete"]:
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to state
        state["messages"].append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Run Agent 1: Profiler 
        with st.chat_message("assistant"):
            with st.spinner("ET Concierge is thinking..."):
                state = run_profiler(state)
                latest_response = state["messages"][-1]["content"]
                st.markdown(latest_response)

        # Run Agent 2 & 3 after profiling complete
        if state["profiling_complete"] and not state["pipeline_complete"]:
            with st.spinner("🔍 Identifying your financial needs..."):
                state = run_identifier(state)

            with st.spinner("📦 Finding best ET products for you..."):
                state = run_recommender(state)

            state["pipeline_complete"] = True

        # Save state back
        st.session_state.state = state
        st.rerun()