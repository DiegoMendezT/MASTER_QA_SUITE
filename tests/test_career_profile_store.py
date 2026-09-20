from utils.career_profile_store import build_profile_from_chat_answers, load_default_profile, save_profile


def test_default_profile_template_is_valid():
    profile = load_default_profile()
    assert "candidate_name" in profile
    assert "core_skills" in profile
    assert "experience" in profile
    assert "sources" in profile


def test_profile_builder_accepts_chat_answers():
    answers = {
        "candidate_name": "Alex Example",
        "current_title": "Senior Python Engineer",
        "core_skills": ["python", "fastapi", "pytest", "sql"]
    }

    profile = build_profile_from_chat_answers(answers)

    assert profile["candidate_name"] == "Alex Example"
    assert profile["current_title"] == "Senior Python Engineer"
    assert "python" in profile["core_skills"]


def test_profile_can_be_saved(tmp_path):
    profile = {"candidate_name": "Jordan", "core_skills": ["python"]}
    target = tmp_path / "profile.json"

    saved = save_profile(profile, target)

    assert saved["candidate_name"] == "Jordan"
    assert target.exists()
