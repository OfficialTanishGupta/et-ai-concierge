from typing import TypedDict, Optional

class UserState(TypedDict):
    # profile of the user
    name: Optional[str]
    age: Optional[int]
    occupation: Optional[str]
    income_range: Optional[str]
    investment_experience: Optional[str]  # three phases as beginner, intermediate, expert
    goals: Optional[list]
    persona: Optional[str]  # new_user, lapsed_user, active_user

    # Conversation mode ongoing
    messages: list
    turn_count: int
    profiling_complete: bool

    # Agent outputs result
    identified_needs: Optional[list]
    recommended_products: Optional[list]
    onboarding_path: Optional[str]

    # Audit trail
    agent_log: list