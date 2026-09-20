from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.career_cv_match import build_alignment_report
from utils.career_cv_pdf import build_curated_cv_text, create_cv_pdf_bytes
from utils.career_profile_extractor import build_profile_from_cv_texts

st.set_page_config(page_title="Career CV MVP", page_icon="📄", layout="wide")

st.title("Career / CV alignment MVP")
st.caption("Truth-first match between a job description and a structured professional profile.")

profile_source = ROOT / "data" / "career_profile_primary_cv_latest.txt"
profile = build_profile_from_cv_texts([profile_source.read_text(encoding="utf-8")])
profile_summary = (
    f"{profile['candidate_name']} is a {profile['current_title']} with skills in "
    f"{', '.join(profile['core_skills'][:10])}."
)

st.subheader("Loaded profile")
st.info(profile_summary)

job_description = st.text_area(
    "Paste the job description",
    height=220,
    value=(
        "Senior Python engineer with FastAPI, pytest, SQL, CI/CD, and mentoring "
        "experience in cloud teams."
    ),
)

if st.button("Run alignment check", type="primary"):
    profile_text_for_match = " ".join([
        profile.get("summary", ""),
        " ".join(profile.get("core_skills", [])),
        " ".join([exp.get("title", "") for exp in profile.get("experience", [])]),
    ])
    report = build_alignment_report(job_description, profile_text_for_match)

    st.subheader("Alignment summary")
    st.metric("Match ratio", f"{report['match_ratio'] * 100:.1f}%")
    st.info(report["verdict"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Matched keywords**")
        if report["matched_keywords"]:
            st.code(", ".join(report["matched_keywords"]))
        else:
            st.write("No overlapping keywords detected.")

    with col2:
        st.markdown("**Missing keywords**")
        if report["missing_keywords"]:
            st.code(", ".join(report["missing_keywords"]))
        else:
            st.write("No missing keywords detected.")

    cv_text = build_curated_cv_text(profile, job_description)
    st.subheader("Tailored CV preview")
    st.text_area("Generated CV content", value=cv_text, height=280, disabled=True)

    pdf_bytes = create_cv_pdf_bytes(cv_text)
    col_pdf, col_txt = st.columns(2)
    with col_pdf:
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="tailored_cv.pdf",
            mime="application/pdf",
        )
    with col_txt:
        st.download_button(
            label="Download TXT",
            data=cv_text,
            file_name="tailored_cv.txt",
            mime="text/plain",
        )
