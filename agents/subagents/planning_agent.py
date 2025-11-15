from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from config import get_llm
from agents.prompts import PLANNING_SYSTEM_PROMPT
from tools.memory_tools import get_profile
from tools.domain_tools import duckduckgo_search


def create_planning_agent():
    """
    ReAct-style planning agent with profile + web search tools.
    """
    llm = get_llm(temperature=0.3)
    tools = [get_profile, duckduckgo_search]
    return create_react_agent(llm, tools)


def run_planning_agent(user_id: str, message: str) -> str:
    """
    Invoke the planning agent and return its final reply text.
    """
    agent = create_planning_agent()
    result = agent.invoke(
        {
            "messages": [
                ("system", PLANNING_SYSTEM_PROMPT),
                HumanMessage(content=f"[user_id={user_id}] {message}"),
            ],
            "user_id": user_id,
        }
    )
    final_msg = result["messages"][-1]
    return final_msg.content

