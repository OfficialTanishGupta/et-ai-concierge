import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

PROFILER_PROMPT = """
You are ET Concierge, a friendly financial assistant for Economic Times.
Your job is to profile the user in maximum 3 conversational turns.

Extract these details naturally through conversation:
- Name
- Age
- Occupation
- Monthly income range (below 30k, 30k-75k, 75k-150k, 150k+)
- Investment experience (beginner, intermediate, expert)
- Financial goals (e.g. save for home, retirement, child education, wealth creation)
- User type (new_user, lapsed_user, active_user)

Rules:
- Be warm, friendly and conversational — not like a form
- Ask maximum 2 questions per turn
- Never use financial jargon with beginners
- Once you have enough info, end your response with: [PROFILE_COMPLETE]

Current conversation:
{chat_history}

User said: {user_message}

Respond naturally and extract profile information:
"""

def run_profiler(state: dict) -> dict:
    """Agent 1: Profiles the user in minimal turns"""
    
    # Build chat history string
    chat_history = ""
    for msg in state["messages"]:
        role = "User" if msg["role"] == "user" else "ET Concierge"
        chat_history += f"{role}: {msg['content']}\n"
    
    # Get last user message
    user_message = state["messages"][-1]["content"] if state["messages"] else ""
    
    # Call Gemini
    prompt = PROFILER_PROMPT.format(
        chat_history=chat_history,
        user_message=user_message
    )
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Check if profiling is complete
    profiling_complete = "[PROFILE_COMPLETE]" in response_text
    clean_response = response_text.replace("[PROFILE_COMPLETE]", "").strip()
    
    # Extract profile details using Gemini
    if profiling_complete:
        extract_prompt = f"""
        Based on this conversation, extract user profile as JSON:
        {chat_history}
        
        Return ONLY a JSON object with these exact keys:
        name, age, occupation, income_range, investment_experience, goals, persona
        
        For persona use: new_user, lapsed_user, or active_user
        For goals use a list of strings
        If any field is unknown use null
        """
        
        extract_response = model.generate_content(extract_prompt)
        
        try:
            import json
            # Clean response to get pure JSON
            json_text = extract_response.text.strip()
            json_text = json_text.replace("```json", "").replace("```", "").strip()
            profile = json.loads(json_text)
            
            # Update state with extracted profile
            state.update({
                "name": profile.get("name"),
                "age": profile.get("age"),
                "occupation": profile.get("occupation"),
                "income_range": profile.get("income_range"),
                "investment_experience": profile.get("investment_experience"),
                "goals": profile.get("goals", []),
                "persona": profile.get("persona", "new_user"),
                "profiling_complete": True
            })
            
            # Log agent action
            state["agent_log"].append({
                "agent": "Profiler",
                "action": "Profile extraction complete",
                "output": profile
            })
            
        except Exception as e:
            state["agent_log"].append({
                "agent": "Profiler", 
                "action": "Profile extraction failed",
                "error": str(e)
            })
    
    # Add response to messages
    state["messages"].append({
        "role": "assistant",
        "content": clean_response
    })
    
    state["turn_count"] = state.get("turn_count", 0) + 1
    
    return state