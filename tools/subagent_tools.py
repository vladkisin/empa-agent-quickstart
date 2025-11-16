from langchain.tools import tool
import logging

from agents.subagents.onboarding_agent import run_onboarding_agent
from agents.subagents.planning_agent import run_planning_agent
from agents.subagents.support_agent import run_support_agent

logger = logging.getLogger(__name__)


@tool
def run_onboarding(user_id: str, message: str) -> str:
    """
    Call the onboarding sub-agent for this user and message.
    Returns a text reply.
    """
    logger.info(f"[TOOL] run_onboarding called with user_id={user_id}, message={message[:100]}...")
    result = run_onboarding_agent(user_id, message)
    logger.info(f"[TOOL] run_onboarding result: {result[:200]}...")
    return result


@tool
def run_planning(user_id: str, message: str) -> str:
    """
    Call the planning sub-agent.
    """
    logger.info(f"[TOOL] run_planning called with user_id={user_id}, message={message[:100]}...")
    result = run_planning_agent(user_id, message)
    logger.info(f"[TOOL] run_planning result: {result[:200]}...")
    return result


@tool
def run_support(user_id: str, message: str) -> str:
    """
    Call the support sub-agent.
    """
    logger.info(f"[TOOL] run_support called with user_id={user_id}, message={message[:100]}...")
    result = run_support_agent(user_id, message)
    logger.info(f"[TOOL] run_support result: {result[:200]}...")
    return result

