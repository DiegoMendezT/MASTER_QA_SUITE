from __future__ import annotations

from typing import Dict, List

from utils.career_cv_match import build_alignment_report


def load_curated_profile() -> Dict[str, object]:
    return {
        "title": "Python Engineer",
        "skills": [
            "python",
            "fastapi",
            "pytest",
            "sql",
            "ci/cd",
            "cloud",
            "kubernetes",
        ],
        "experience": [
            "Built APIs with FastAPI and Python.",
            "Automated test coverage with pytest and CI/CD pipelines.",
            "Worked with cloud-hosted services and SQL-backed systems.",
        ],
    }


def profile_to_text(profile: Dict[str, object]) -> str:
    title = str(profile.get("title", ""))
    skills = ", ".join(str(skill) for skill in profile.get("skills", []))
    experience = " ".join(str(item) for item in profile.get("experience", []))
    return f"{title}. Skills: {skills}. Experience: {experience}."


def score_profile(job_description: str, profile: Dict[str, object]) -> Dict[str, object]:
    cv_text = profile_to_text(profile)
    report = build_alignment_report(job_description, cv_text)
    return {
        "matched_keywords": report["matched_keywords"],
        "missing_keywords": report["missing_keywords"],
        "match_ratio": report["match_ratio"],
        "verdict": report["verdict"],
    }
