from langchain.tools import tool
import json

from agents.storage import storage, UserProfile


@tool
def get_profile(user_id: str) -> str:
    """
    Get the user's profile as a JSON string.
    """
    profile = storage.load_profile(user_id)
    return profile.model_dump_json()


@tool
def save_profile(user_id: str, profile_json: str) -> str:
    """
    Save the user's profile from a JSON string.
    Returns a short status message.
    """
    data = json.loads(profile_json)
    profile = UserProfile.model_validate(data)
    storage.save_profile(profile)
    return "Profile saved"

