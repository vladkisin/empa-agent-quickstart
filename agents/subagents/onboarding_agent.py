from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from config import get_llm
from agents.prompts import ONBOARDING_SYSTEM_PROMPT
from tools.memory_tools import get_profile, update_habit


def create_onboarding_agent():
    """
    ReAct-style onboarding agent with access to profile tools.
    """
    llm = get_llm(temperature=0.4)
    tools = [get_profile, update_habit]
    agent = create_react_agent(llm, tools)
    agent.system_prompt = ONBOARDING_SYSTEM_PROMPT  # type: ignore[attr-defined]
    return agent


def run_onboarding_agent(user_id: str, message: str) -> str:
    """
    Invoke the onboarding agent and return its final reply text.
    """
    agent = create_onboarding_agent()
    system_with_user = f"{ONBOARDING_SYSTEM_PROMPT}\n\nCurrent user_id: {user_id}"
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

