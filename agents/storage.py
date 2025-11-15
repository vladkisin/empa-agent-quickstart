from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from config import DATA_DIR


class HabitData(BaseModel):
    description: Optional[str] = None  # WHAT
    cue: Optional[str] = None          # WHEN/WHERE
    action: Optional[str] = None       # tiny behavior
    reward: Optional[str] = None       # small nice thing
    motivation: Optional[str] = None   # WHY


class HabitStats(BaseModel):
    attempts: int = 0
    successes: int = 0
    last_report: Optional[str] = None


class UserProfile(BaseModel):
    user_id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    habit: HabitData = Field(default_factory=HabitData)
    stats: HabitStats = Field(default_factory=HabitStats)


class Storage:
    """
    JSON-file-based storage:
    - data/profiles/<user_id>.json
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or DATA_DIR
        self.profiles_dir = self.base_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def _profile_path(self, user_id: str) -> Path:
        return self.profiles_dir / f"{user_id}.json"

    def load_profile(self, user_id: str) -> UserProfile:
        path = self._profile_path(user_id)
        if not path.exists():
            return UserProfile(user_id=user_id)
        raw = path.read_text(encoding="utf-8")
        return UserProfile.model_validate_json(raw)

    def save_profile(self, profile: UserProfile) -> None:
        profile.updated_at = datetime.utcnow().isoformat()
        path = self._profile_path(profile.user_id)
        path.write_text(profile.model_dump_json(indent=2), encoding="utf-8")


storage = Storage()

