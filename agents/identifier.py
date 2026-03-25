from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

IDENTIFIER_PROMPT = """
You are a financial needs analyst for Economic Times.
Based on the user profile below, identify their top 3 financial needs.

User Profile:
- Name: {name}
- Age: {age}
- Occupation: {occupation}
- Income Range: {income_range}
- Investment Experience: {investment_experience}
- Goals: {goals}
- User Type: {persona}

Rules:
- Be specific, not generic
- Consider their age, income and experience level together
- For new_user: focus on education and simple first steps
- For lapsed_user: focus on what they missed and new value
- For active_user: focus on advanced tools and cross-sell

Return ONLY a JSON array of exactly 3 needs like this:
[
  {{
    "need": "need title",
    "reason": "why this user needs this",
    "priority": "high/medium/low"
  }}
]
"""

def run_identifier(state: dict) -> dict:
    """Agent 2: Identifies user's top financial needs from profile"""

    prompt = IDENTIFIER_PROMPT.format(
        name=state.get("name", "User"),
        age=state.get("age", "unknown"),
        occupation=state.get("occupation", "unknown"),
        income_range=state.get("income_range", "unknown"),
        investment_experience=state.get("investment_experience", "beginner"),
        goals=", ".join(state.get("goals", [])),
        persona=state.get("persona", "new_user")
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        json_text = response.text.strip()
        json_text = json_text.replace("```json", "").replace("```", "").strip()
        needs = json.loads(json_text)

        state["identified_needs"] = needs
        state["agent_log"].append({
            "agent": "Identifier",
            "action": "Needs identification complete",
            "output": needs
        })

    except Exception as e:
        state["identified_needs"] = [
            {
                "need": "Basic Investment Education",
                "reason": "User needs foundational knowledge",
                "priority": "high"
            },
            {
                "need": "Portfolio Tracking",
                "reason": "User needs to monitor investments",
                "priority": "medium"
            },
            {
                "need": "Financial Planning",
                "reason": "User needs a structured financial plan",
                "priority": "medium"
            }
        ]
        state["agent_log"].append({
            "agent": "Identifier",
            "action": "Needs identification failed, using fallback",
            "error": str(e)
        })

    return state
