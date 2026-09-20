from __future__ import annotations

from io import BytesIO
from typing import Dict, List


def build_curated_cv_text(profile: Dict[str, object], job_description: str) -> str:
    name = str(profile.get("candidate_name", "Candidate"))
    title = str(profile.get("current_title", "Professional"))
    summary = str(profile.get("summary", "")).strip()
    skills = [str(skill) for skill in profile.get("core_skills", []) if str(skill).strip()]
    experience_entries = profile.get("experience", [])

    experience_items: List[str] = []
    for entry in experience_entries:
        if not isinstance(entry, dict):
            continue
        company = str(entry.get("company", "")).strip()
        role = str(entry.get("title", "")).strip()
        dates = str(entry.get("dates", "")).strip()
        responsibilities = entry.get("responsibilities", [])
        if company or role or dates:
            experience_items.append(f"{company} | {role} | {dates}")
            for responsibility in responsibilities[:3]:
                if str(responsibility).strip():
                    experience_items.append(f"  - {str(responsibility).strip()}")
            experience_items.append("")

    cv_sections = [
        name,
        title,
        "",
        "Professional Summary",
        "-" * 20,
        summary,
        "",
        "Core Skills",
        "-" * 20,
        ", ".join(skills[:20]),
        "",
        "Experience",
        "-" * 20,
        *experience_items,
        "Target Role Fit",
        "-" * 20,
        f"This profile is aligned to a role emphasizing: {job_description[:250]}",
    ]
    return "\n".join(cv_sections)


def create_cv_pdf_bytes(cv_text: str) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Career CV")
    pdf.setAuthor("MASTER_QA_SUITE")
    pdf.setFont("Helvetica", 11)

    y = 760
    for line in cv_text.splitlines():
        pdf.drawString(72, y, line[:110])
        y -= 16
        if y < 60:
            pdf.showPage()
            y = 760

    pdf.save()
    return buffer.getvalue()
