from typing import TypedDict, Optional

class UserState(TypedDict):
    # User profile
    name: Optional[str]
    age: Optional[int]
    occupation: Optional[str]
    income_range: Optional[str]
    investment_experience: Optional[str]
    goals: Optional[list]
    persona: Optional[str]

    # Conversation
    messages: list
    turn_count: int
    profiling_complete: bool

    # Agent 2 outputs
    identified_needs: Optional[list]
    financial_scores: Optional[dict]
    overall_score: Optional[int]
    monthly_savings_target: Optional[str]
    gap_analysis: Optional[str]
    financial_analysis: Optional[dict]

    # Agent 3 outputs
    recommended_products: Optional[list]
    onboarding_path: Optional[str]

    # Pipeline
    identifier_complete: bool
    pipeline_complete: bool

    # Audit trail
    agent_log: list