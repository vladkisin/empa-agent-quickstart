from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from config import get_llm
from agents.prompts import ONBOARDING_SYSTEM_PROMPT
from tools.memory_tools import get_profile


def create_onboarding_agent():
    """
    ReAct-style onboarding agent with access to profile tools.
    """
    llm = get_llm(temperature=0.4)
    tools = [get_profile]
    return create_react_agent(llm, tools)


def run_onboarding_agent(user_id: str, message: str) -> str:
    """
    Invoke the onboarding agent and return its final reply text.
    """
    agent = create_onboarding_agent()
    result = agent.invoke(
        {
            "messages": [
                ("system", ONBOARDING_SYSTEM_PROMPT),
                HumanMessage(content=f"[user_id={user_id}] {message}"),
            ],
            "user_id": user_id,
        }
    )
    final_msg = result["messages"][-1]
    return final_msg.content

