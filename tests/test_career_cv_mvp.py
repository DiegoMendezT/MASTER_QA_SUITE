from utils.career_cv_match import build_alignment_report, extract_keywords
from utils.career_cv_profile import load_curated_profile, profile_to_text, score_profile


def test_extract_keywords_returns_relevant_terms():
    job_description = (
        "Senior Python engineer with FastAPI, pytest, SQL, CI/CD, and mentoring "
        "experience in cloud teams."
    )

    keywords = extract_keywords(job_description)

    assert "python" in keywords
    assert "fastapi" in keywords
    assert "pytest" in keywords
    assert "sql" in keywords
    assert "ci" in keywords


def test_build_alignment_report_identifies_matches_and_gaps():
    job_description = (
        "We need a Python engineer with FastAPI, pytest, SQL, CI/CD, mentoring, "
        "and Kubernetes experience working across cloud and distributed teams."
    )
    cv_text = (
        "Python developer with experience in FastAPI, pytest, CI/CD automation, and SQL. "
        "Worked with cloud teams and distributed engineering workflows."
    )

    report = build_alignment_report(job_description, cv_text)

    assert report["match_ratio"] > 0.5
    assert "python" in report["matched_keywords"]
    assert "fastapi" in report["matched_keywords"]
    assert "sql" in report["matched_keywords"]
    assert "kubernetes" in report["missing_keywords"]
    assert "mentoring" in report["missing_keywords"]
    assert "verdict" in report


def test_curated_profile_is_loaded_and_scored():
    profile = load_curated_profile()
    assert profile["title"].lower().startswith("python")
    assert "python" in profile["skills"]

    cv_text = profile_to_text(profile)
    assert "fastapi" in cv_text.lower()

    score = score_profile(
        "Python engineer with FastAPI, pytest, SQL, and CI/CD experience.",
        profile,
    )
    assert score["match_ratio"] > 0.5
    assert score["verdict"] in {"Strong fit", "Needs tailoring"}
