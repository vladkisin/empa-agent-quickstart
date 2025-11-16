from langchain.tools import tool
import json
import logging

from agents.storage import storage, UserProfile

logger = logging.getLogger(__name__)


@tool
def get_profile(user_id: str) -> str:
    """
    Get the user's profile as a JSON string.
    """
    logger.info(f"[TOOL] get_profile called with user_id={user_id}")
    profile = storage.load_profile(user_id)
    result = profile.model_dump_json()
    logger.info(f"[TOOL] get_profile result: {result[:200]}...")
    return result


@tool
def save_profile(user_id: str, profile_json: str) -> str:
    """
    Save the user's profile from a JSON string.
    Returns a short status message.
    """
    logger.info(f"[TOOL] save_profile called with user_id={user_id}, profile_json length={len(profile_json)}")
    data = json.loads(profile_json)
    profile = UserProfile.model_validate(data)
    storage.save_profile(profile)
    result = "Profile saved"
    logger.info(f"[TOOL] save_profile result: {result}")
    return result

@tool
def update_habit(
    user_id: str,
    description: str | None = None,
    motivation: str | None = None,
    cue: str | None = None,
    action: str | None = None,
    reward: str | None = None,
) -> str:
    """
    Update one or more fields of the user's habit and persist the profile.

    Any field left as None will be preserved.
    Returns a short text summary of the updated habit.
    """
    logger.info(
        f"[TOOL] update_habit called with user_id={user_id}, "
        f"description={description}, motivation={motivation}, "
        f"cue={cue}, action={action}, reward={reward}"
    )
    profile = storage.load_profile(user_id)

    if description is not None:
        profile.habit.description = description
    if motivation is not None:
        profile.habit.motivation = motivation
    if cue is not None:
        profile.habit.cue = cue
    if action is not None:
        profile.habit.action = action
    if reward is not None:
        profile.habit.reward = reward

    storage.save_profile(profile)

    summary = (
        f"Habit: {profile.habit.description!r}, "
        f"motivation={profile.habit.motivation!r}, "
        f"cue={profile.habit.cue!r}, action={profile.habit.action!r}, "
        f"reward={profile.habit.reward!r}"
    )
    logger.info(f"[TOOL] update_habit summary: {summary}")
    return summary


@tool
def update_plan(user_id: str, description: str) -> str:
    """
    Update the plan description for the user and persist the profile.
    
    This saves a version of the plan description that summarizes the habit plan.
    Returns a confirmation message with the saved plan description.
    """
    logger.info(
        f"[TOOL] update_plan called with user_id={user_id}, description length={len(description)}"
    )
    profile = storage.load_profile(user_id)
    profile.plan.description = description
    storage.save_profile(profile)
    
    result = f"Plan saved: {description[:100]}..." if len(description) > 100 else f"Plan saved: {description}"
    logger.info(f"[TOOL] update_plan result: {result}")
    return result


@tool
def log_attempt(user_id: str, success: bool, note: str | None = None) -> str:
    """
    Log one habit attempt for the user and persist stats.
    """
    from datetime import datetime

    logger.info(
        f"[TOOL] log_attempt called with user_id={user_id}, success={success}, note={note}"
    )
    profile = storage.load_profile(user_id)
    profile.stats.attempts += 1
    if success:
        profile.stats.successes += 1
    profile.stats.last_report = datetime.utcnow().isoformat()
    storage.save_profile(profile)

    rate = (
        profile.stats.successes / profile.stats.attempts
        if profile.stats.attempts > 0
        else 0.0
    )
    summary = (
        f"Attempts={profile.stats.attempts}, successes={profile.stats.successes}, "
        f"success_rate={rate:.2f}"
    )
    logger.info(f"[TOOL] log_attempt summary: {summary}")
    return summary
