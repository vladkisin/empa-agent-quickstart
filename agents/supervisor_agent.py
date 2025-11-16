from langgraph.prebuilt import create_react_agent

from config import get_llm
from agents.prompts import SUPERVISOR_SYSTEM_PROMPT
from tools.memory_tools import get_profile, save_profile, update_habit
from tools.subagent_tools import run_onboarding, run_planning, run_support


def create_supervisor_agent():
    """
    Supervisor ReAct agent.

    Tools:
    - get_profile, save_profile (memory)
    - run_onboarding, run_planning, run_support (sub-agents)
    """
    llm = get_llm(temperature=0.3)
    tools = [get_profile, update_habit, run_onboarding, run_planning, run_support]
    agent = create_react_agent(llm, tools)
    agent.system_prompt = SUPERVISOR_SYSTEM_PROMPT  # type: ignore[attr-defined]
    return agent


