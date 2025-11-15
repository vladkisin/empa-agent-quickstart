from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState


def create_graph():
    # TODO: add nodes (supervisor, memory, etc.)
    workflow = StateGraph(AgentState)
    workflow.set_entry_point("placeholder")
    workflow.add_edge("placeholder", END)
    return workflow.compile(checkpointer=MemorySaver())

