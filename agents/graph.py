from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
import logging

from .state import AgentState
from .supervisor_agent import create_supervisor_agent
from .prompts import SUPERVISOR_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def supervisor_node(state: AgentState) -> AgentState:
    agent = create_supervisor_agent()

    prior = state.get("messages", [])
    system_content = f"{SUPERVISOR_SYSTEM_PROMPT}\n\nCurrent user_id: {state['user_id']}"
    msgs = [SystemMessage(content=system_content)] + prior
    msgs.append(HumanMessage(content=state["user_message"]))

    logger.info(f"[AI] User message: {state['user_message']}")
    
    result = agent.invoke({"messages": msgs, "user_id": state["user_id"]}, config={"configurable": {"user_id": state["user_id"]}})
    
    # Log all messages from agent execution
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            logger.info(f"[AI] AI message: {msg.content[:500]}...")
        elif isinstance(msg, ToolMessage):
            logger.info(f"[AI] Tool message from {getattr(msg, 'name', 'unknown')}: {msg.content[:200]}...")
    
    final_msg = result["messages"][-1]

    state["messages"] = result["messages"]
    state["response"] = final_msg.content
    state["user_id"] = state["user_id"]
    return state


def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("supervisor", supervisor_node)
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", END)
    app = workflow.compile(checkpointer=MemorySaver())
    return app

