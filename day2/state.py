from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    topic: str
    problem: str
    answer: str
    submissions: Annotated[list[str], operator.add]
    scores: Annotated[list[float], operator.add]
    hints_given: Annotated[list[str], operator.add]