from pathlib import Path

from utils.career_profile_extractor import build_profile_from_cv_texts


def test_build_profile_from_cv_texts_extracts_identity_and_skills():
    text = Path("data/career_profile_primary_cv_latest.txt").read_text(encoding="utf-8")

    profile = build_profile_from_cv_texts([text])

    assert profile["candidate_name"]
    assert "python" in [skill.lower() for skill in profile["core_skills"]]
    assert "selenium" in [skill.lower() for skill in profile["core_skills"]]
    assert len(profile["experience"]) >= 3
    assert "summary" in profile
