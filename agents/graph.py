from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage

from .state import AgentState
from .supervisor_agent import create_supervisor_agent
from .prompts import SUPERVISOR_SYSTEM_PROMPT


def supervisor_node(state: AgentState) -> AgentState:
    agent = create_supervisor_agent()

    prior = state.get("messages", [])
    msgs = [SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)] + prior
    msgs.append(HumanMessage(content=state["user_message"]))

    result = agent.invoke({"messages": msgs, "user_id": state["user_id"]})
    final_msg = result["messages"][-1]

    state["messages"] = result["messages"]
    state["response"] = final_msg.content
    return state


def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor_node)
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", END)
    app = workflow.compile(checkpointer=MemorySaver())
    return app

