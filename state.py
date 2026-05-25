from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    topic: str
    draft: str
    submissions: Annotated[list[str], operator.add]
    scores: Annotated[list[float], operator.add]
    hints_given: Annotated[list[str], operator.add]