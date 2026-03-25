from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

IDENTIFIER_PROMPT = """
You are a Financial Analysis Agent for Economic Times.
Analyse the user profile below and produce a detailed financial assessment.

User Profile:
- Name: {name}
- Age: {age}
- Occupation: {occupation}
- Monthly Income Range: {income_range}
- Investment Experience: {investment_experience}
- Goals: {goals}
- User Type: {persona}

Your job is to:
1. Score the user across 4 financial dimensions (0-10 each)
2. Identify top 3 financial needs with priority and reasoning
3. Calculate a simple financial gap analysis
4. Suggest a realistic monthly savings target

Return ONLY a JSON object like this:
{{
  "financial_scores": {{
    "emergency_preparedness": {{
      "score": 3,
      "insight": "direct insight written to user using you/your"
    }},
    "investment_readiness": {{
      "score": 5,
      "insight": "direct insight written to user using you/your"
    }},
    "goal_clarity": {{
      "score": 7,
      "insight": "direct insight written to user using you/your"
    }},
    "financial_awareness": {{
      "score": 4,
      "insight": "direct insight written to user using you/your"
    }}
  }},
  "overall_score": 5,
  "monthly_savings_target": "₹8,000 - ₹12,000",
  "gap_analysis": "direct 1-2 sentence gap analysis written to user using you/your",
  "identified_needs": [
    {{
      "need": "need title",
      "reason": "reason written directly to user using you/your",
      "priority": "high/medium/low",
      "estimated_impact": "what solving this does for the user"
    }}
  ]
}}

Important rules:
- Write ALL text directly to the user using you/your — never say the user or their name in third person
- Be specific with numbers where possible
- Keep insights short and actionable
"""

def run_identifier(state: dict) -> dict:
    """Agent 2: Deep financial analysis — scores, gap analysis, needs identification"""

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
        analysis = json.loads(json_text)

        # Store full analysis in state
        state["financial_analysis"] = analysis
        state["identified_needs"] = analysis.get("identified_needs", [])
        state["financial_scores"] = analysis.get("financial_scores", {})
        state["overall_score"] = analysis.get("overall_score", 0)
        state["monthly_savings_target"] = analysis.get("monthly_savings_target", "")
        state["gap_analysis"] = analysis.get("gap_analysis", "")

        state["agent_log"].append({
            "agent": "Identifier",
            "action": "Deep financial analysis complete",
            "output": analysis
        })

    except Exception as e:
        state["identified_needs"] = [
            {
                "need": "Emergency Fund Setup",
                "reason": "Building a safety net should be your first financial priority",
                "priority": "high",
                "estimated_impact": "Protects you from financial shocks"
            }
        ]
        state["financial_scores"] = {}
        state["overall_score"] = 0
        state["gap_analysis"] = ""
        state["monthly_savings_target"] = ""

        state["agent_log"].append({
            "agent": "Identifier",
            "action": "Analysis failed, using fallback",
            "error": str(e)
        })

    return state