from typing import TypedDict, Annotated, List, Any
import operator


class AgentState(TypedDict):
    """
    Core LangGraph state for one conversation instance.

    We intentionally do NOT embed the long-term profile here to avoid
    duplicating it in the checkpointer. Profile is handled via tools and storage.
    """
    user_id: str
    user_message: str
    messages: Annotated[List[Any], operator.add]
    response: str

