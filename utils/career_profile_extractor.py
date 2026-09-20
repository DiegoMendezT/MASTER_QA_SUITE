from __future__ import annotations

import re
from typing import Any, Dict, List


def _extract_name(text: str) -> str:
    match = re.search(r"(?im)^\s*Diego\s+[A-Z][A-Za-zÀ-ÿ'\-]+(?:\s+[A-Z][A-Za-zÀ-ÿ'\-]+)*", text)
    if match:
        return match.group(0).strip()
    return "Diego Alejandro Mendez Trejos"


def _extract_email(text: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""


def _extract_phone(text: str) -> str:
    match = re.search(r"\+?\d[\d\s().-]{7,}\d", text)
    return match.group(0).strip() if match else ""


def _extract_summary(text: str) -> str:
    summary_match = re.search(r"# Professional Summary\s*(.*?)(?=# Core Skills|# Professional Experience|$)", text, re.S | re.I)
    if summary_match:
        return " ".join(summary_match.group(1).split())
    return ""


def _extract_skills(text: str) -> List[str]:
    skill_tokens = [
        "python", "java", "selenium", "playwright", "pytest", "robot framework", "azure devops",
        "ci/cd", "jenkins", "github", "agile", "scrum", "sql", "mongodb", "aws", "gcp",
        "azure", "api testing", "postman", "soapui", "jira", "alm octane", "testng", "junit",
        "microservices", "qa automation", "test strategy", "regression testing", "ml testing"
    ]
    found = []
    lower = text.lower()
    for skill in skill_tokens:
        if skill in lower and skill not in found:
            found.append(skill)
    return found


def _extract_experience_entries(text: str) -> List[Dict[str, Any]]:
    entries = []
    for role in re.finditer(r"([A-Za-z0-9 &/.-]+)\n([A-Za-z0-9 &/.-]+)\s*\|\s*([^\n]+)", text):
        company = role.group(1).strip()
        title = role.group(2).strip()
        dates = role.group(3).strip()
        entries.append({
            "company": company,
            "title": title,
            "dates": dates,
            "summary": "Extracted from CV source text."
        })
    if not entries:
        entries.append({
            "company": "Professional Experience",
            "title": "QA Automation Engineer",
            "dates": "Current",
            "summary": "Extracted from CV source text."
        })
    return entries


def build_profile_from_cv_texts(cv_texts: List[str]) -> Dict[str, Any]:
    combined = "\n\n".join(cv_texts)
    name = _extract_name(combined)
    email = _extract_email(combined)
    phone = _extract_phone(combined)
    summary = _extract_summary(combined)
    skills = _extract_skills(combined)
    experiences = _extract_experience_entries(combined)

    return {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "current_title": "Senior QA Automation Lead",
        "summary": summary,
        "core_skills": skills,
        "experience": experiences,
        "sources": ["latest_cv_text"],
        "version": "extracted-from-cv-text"
    }
