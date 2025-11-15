from langchain.tools import tool

from agents.subagents.onboarding_agent import run_onboarding_agent
from agents.subagents.planning_agent import run_planning_agent
from agents.subagents.support_agent import run_support_agent


@tool
def run_onboarding(user_id: str, message: str) -> str:
    """
    Call the onboarding sub-agent for this user and message.
    Returns a text reply.
    """
    return run_onboarding_agent(user_id, message)


@tool
def run_planning(user_id: str, message: str) -> str:
    """
    Call the planning sub-agent.
    """
    return run_planning_agent(user_id, message)


@tool
def run_support(user_id: str, message: str) -> str:
    """
    Call the support sub-agent.
    """
    return run_support_agent(user_id, message)

