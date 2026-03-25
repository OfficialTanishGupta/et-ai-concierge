from google import genai
import os
import json
from dotenv import load_dotenv
from utils.et_products import ET_PRODUCTS

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

RECOMMENDER_PROMPT = """
You are an ET product recommendation expert.
Based on the user profile and their identified needs, recommend the best ET products.

User Profile:
- Name: {name}
- Age: {age}
- Investment Experience: {investment_experience}
- Goals: {goals}
- User Type: {persona}

Identified Needs:
{needs}

Available ET Products:
{products}

Rules:
- Recommend exactly 2-3 most relevant products
- Match products to identified needs specifically
- For new_user: keep it simple, max 2 products
- For lapsed_user: highlight what is new since they left
- For active_user: suggest advanced or cross-sell products
- Never recommend more than 3 products at once
- If user searched for home loan or property, always include ET Financial Services - Home Loan
- Never mention competitor platforms

Return ONLY a JSON array like this:
[
  {{
    "product": "product name",
    "reason": "specific reason for this user",
    "action": "exact first step for user to take",
    "priority": 1
  }}
]
"""

ONBOARDING_PROMPT = """
You are ET Concierge, a warm and helpful assistant.
Based on these product recommendations, write a friendly onboarding message for {name}.

Recommendations:
{recommendations}

User Type: {persona}
Investment Experience: {investment_experience}

Rules:
- Be warm and personal, use their name
- Keep it under 100 words
- Give them ONE clear next step
- For beginner: use simple language, no jargon
- For lapsed_user: acknowledge they were away, welcome them back
- For active_user: be professional and highlight new value
- End with an encouraging sentence
"""

def run_recommender(state: dict) -> dict:
    """Agent 3: Recommends ET products and creates onboarding path"""

    needs_text = json.dumps(state.get("identified_needs", []), indent=2)
    products_text = json.dumps(ET_PRODUCTS, indent=2)

    prompt = RECOMMENDER_PROMPT.format(
        name=state.get("name", "User"),
        age=state.get("age", "unknown"),
        investment_experience=state.get("investment_experience", "beginner"),
        goals=", ".join(state.get("goals", [])),
        persona=state.get("persona", "new_user"),
        needs=needs_text,
        products=products_text
    )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        json_text = response.text.strip()
        json_text = json_text.replace("```json", "").replace("```", "").strip()
        recommendations = json.loads(json_text)

        state["recommended_products"] = recommendations
        state["agent_log"].append({
            "agent": "Recommender",
            "action": "Product recommendations complete",
            "output": recommendations
        })

        onboarding_prompt = ONBOARDING_PROMPT.format(
            name=state.get("name", "User"),
            recommendations=json.dumps(recommendations, indent=2),
            persona=state.get("persona", "new_user"),
            investment_experience=state.get("investment_experience", "beginner")
        )

        onboarding_response = client.models.generate_content(
            model=MODEL,
            contents=onboarding_prompt
        )
        state["onboarding_path"] = onboarding_response.text.strip()

        state["agent_log"].append({
            "agent": "Recommender",
            "action": "Onboarding path created",
            "output": state["onboarding_path"]
        })

    except Exception as e:
        state["recommended_products"] = [
            {
                "product": "ET Money",
                "reason": "Best starting point for new investors",
                "action": "Download ET Money app and start your first SIP",
                "priority": 1
            }
        ]
        state["onboarding_path"] = f"Welcome to ET, {state.get('name', 'there')}! Start your journey with ET Money — India's simplest investing app."
        state["agent_log"].append({
            "agent": "Recommender",
            "action": "Recommendation failed, using fallback",
            "error": str(e)
        })

    return state
