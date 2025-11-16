from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from config import get_llm
from agents.prompts import PLANNING_SYSTEM_PROMPT
from tools.memory_tools import get_profile, update_plan
from tools.domain_tools import duckduckgo_search


def create_planning_agent():
    """
    ReAct-style planning agent with profile + web search + plan update tools.
    """
    llm = get_llm(temperature=0.3)
    tools = [get_profile, update_plan, duckduckgo_search]
    agent = create_react_agent(llm, tools)
    agent.system_prompt = PLANNING_SYSTEM_PROMPT  # type: ignore[attr-defined]
    return agent


def run_planning_agent(user_id: str, message: str) -> str:
    """
    Invoke the planning agent and return its final reply text.
    """
    agent = create_planning_agent()
    system_with_user = f"{PLANNING_SYSTEM_PROMPT}\n\nCurrent user_id: {user_id}"
    result = agent.invoke(
        {
            "messages": [
                SystemMessage(content=system_with_user),
                HumanMessage(content=message),
            ],
            "user_id": user_id,
        },
        config={"configurable": {"user_id": user_id}}
    )
    final_msg = result["messages"][-1]
    return final_msg.content


