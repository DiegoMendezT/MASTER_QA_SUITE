from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

PROFILE_PATH = Path(__file__).resolve().parents[1] / "data" / "career_profile_template.json"


def load_default_profile() -> Dict[str, Any]:
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_profile(profile: Dict[str, Any], path: str | Path | None = None) -> Dict[str, Any]:
    target = Path(path) if path else PROFILE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(profile, file, indent=2, ensure_ascii=False)
    return profile


def build_profile_from_chat_answers(answers: Dict[str, Any]) -> Dict[str, Any]:
    profile = load_default_profile()
    for key, value in answers.items():
        if key in profile:
            profile[key] = value
    return profile
