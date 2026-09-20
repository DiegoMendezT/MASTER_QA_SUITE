from pathlib import Path

from pypdf import PdfReader

from utils.career_cv_pdf import build_curated_cv_text, create_cv_pdf_bytes


def test_build_curated_cv_text_uses_profile_and_job_context():
    profile = {
        "candidate_name": "Diego Alejandro Mendez Trejos",
        "current_title": "Senior QA Automation Lead",
        "summary": "Results-driven QA Automation Engineer with 15 years of experience.",
        "core_skills": ["Python", "Selenium", "CI/CD", "Azure DevOps"],
        "experience": [
            {"company": "Edwards Lifesciences", "title": "QA Engineer", "dates": "2025-2026"},
            {"company": "TransUnion", "title": "QA Lead", "dates": "2025"},
        ],
    }
    job_description = "Senior QA Automation Lead with Python, Selenium, Azure DevOps, and CI/CD experience."

    cv_text = build_curated_cv_text(profile, job_description)

    assert "Diego Alejandro Mendez Trejos" in cv_text
    assert "Professional Summary" in cv_text
    assert "Results-driven QA Automation Engineer" in cv_text
    assert "Core Skills" in cv_text
    assert "Python" in cv_text
    assert "Selenium" in cv_text
    assert "CI/CD" in cv_text
    assert "Edwards Lifesciences" in cv_text
    assert "Target Role Fit" in cv_text
    assert "Senior QA Automation Lead" in cv_text


def test_create_cv_pdf_bytes_returns_pdf_payload():
    cv_text = "Diego Alejandro\nSenior QA Automation Lead\nPython, Selenium, CI/CD"

    pdf_bytes = create_cv_pdf_bytes(cv_text)

    assert pdf_bytes.startswith(b"%PDF")
    reader = PdfReader(__import__('io').BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "Diego Alejandro" in text
    assert "Senior QA Automation Lead" in text
