from __future__ import annotations

import re
from typing import Dict, List

STOP_WORDS = {
    "a", "an", "and", "any", "are", "as", "at", "be", "by", "for", "from",
    "have", "in", "into", "is", "it", "its", "of", "on", "or", "our", "that",
    "the", "their", "them", "there", "these", "they", "this", "to", "we", "with",
    "work", "worked", "working", "across", "need", "needs", "using", "used", "within",
    "across", "about", "after", "before", "between", "through", "under", "over",
    "where", "when", "while", "who", "which", "why", "how", "than", "then", "also",
    "experience", "experiences"
}


def normalize_keyword(keyword: str) -> str:
    value = keyword.lower().strip()
    value = value.replace("/", " ")
    value = re.sub(r"[^a-z0-9\s-]", " ", value)
    parts = [part for part in re.split(r"\s+|-+", value) if part]
    return parts


def extract_keywords(text: str) -> List[str]:
    raw_tokens = re.findall(r"[a-zA-Z0-9]+(?:[./-][a-zA-Z0-9]+)*", text)
    keywords: List[str] = []
    for token in raw_tokens:
        normalized_parts = normalize_keyword(token)
        for part in normalized_parts:
            if len(part) < 2:
                continue
            if part in STOP_WORDS:
                continue
            if part not in keywords:
                keywords.append(part)
    return keywords


def build_alignment_report(job_description: str, cv_text: str) -> Dict[str, object]:
    job_keywords = extract_keywords(job_description)
    cv_keywords = extract_keywords(cv_text)
    cv_keyword_set = set(cv_keywords)

    matched = [keyword for keyword in job_keywords if keyword in cv_keyword_set]
    missing = [keyword for keyword in job_keywords if keyword not in cv_keyword_set]

    match_ratio = 0.0
    if job_keywords:
        match_ratio = len(matched) / len(job_keywords)

    verdict = "Strong fit" if match_ratio >= 0.5 else "Needs tailoring"

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "match_ratio": round(match_ratio, 3),
        "verdict": verdict,
    }
