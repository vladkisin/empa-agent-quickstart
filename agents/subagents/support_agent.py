from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime

from config import get_llm
from agents.prompts import SUPPORT_SYSTEM_PROMPT
from tools.memory_tools import get_profile, log_attempt
from agents.storage import storage


def create_support_agent():
    """
    ReAct-style support agent with profile tools.
    """
    llm = get_llm(temperature=0.5)
    tools = [get_profile, log_attempt]
    agent = create_react_agent(llm, tools)
    agent.system_prompt = SUPPORT_SYSTEM_PROMPT  # type: ignore[attr-defined]
    return agent


def run_support_agent(user_id: str, message: str) -> str:
    """
    Invoke the support agent and return its final reply text.

    Also heuristically update attempts/successes before calling the agent.
    """
    profile = storage.load_profile(user_id)
    text = message.lower()
    success = None
    if "did it" in text or "completed" in text or "success" in text:
        success = True
    elif "didn't" in text or "failed" in text or "couldn't" in text:
        success = False

    if success is True:
        profile.stats.attempts += 1
        profile.stats.successes += 1
    elif success is False:
        profile.stats.attempts += 1

    if success is not None:
        profile.stats.last_report = datetime.utcnow().isoformat()
        storage.save_profile(profile)

    agent = create_support_agent()
    system_with_user = f"{SUPPORT_SYSTEM_PROMPT}\n\nCurrent user_id: {user_id}"
    result = agent.invoke(
        {
            "messages": [
                SystemMessage(content=system_with_user),
                HumanMessage(
                    content=(
                        f"(Attempts={profile.stats.attempts}, "
                        f"Successes={profile.stats.successes}) "
                        f"{message}"
                    )
                ),
            ],
            "user_id": user_id,
        },
        config={"configurable": {"user_id": user_id}}
    )
    final_msg = result["messages"][-1]
    return final_msg.content


