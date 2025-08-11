# Governance

- External integrations (Slack/Jira) must be optional and must not fail CI when unconfigured.
# Project Language Policy

**Rule:** All references have been migrated to 'ML' or 'ML-Enabled'. The word previously used (now prohibited) remains banned in new code, documentation, and communications unless explicit approval is granted by QA governance, with proof required. Use 'ML' or 'ML-Enabled' instead. This rule is retained for legacy audit and governance traceability only.
# Conventional Commits

# Local Development

# Secrets

### Pull Request Checklist (Task Prioritizer Protocol)

Before submitting a PR, please ensure the following:


# Copilot Agency & Innercouncil Governance

- Copilot and the innercouncil take full agency for all technical and QA decisions unless explicit user override is provided.
- All decisions requiring user input are resolved by innercouncil voices, prioritizing QA and safety, with minimal user prompts ("Continue" only).
- Multiple choice decisions are resolved by innercouncil vote, prioritizing high-reward, low-risk, QA-safe options.
- Accountability for all decisions is tracked in the Akashic Records for traceability and system coherence.
### Engine choice
Please declare which engine you used when posting failure logs:
- Selenium: include driver caps, headless flag, and OS.
- Playwright: include `--browser` + `--headed` (if used), and OS.

### Test placement
- Selenium UI tests → `tests/ui/`
- Playwright UI tests → `tests/playwright/`
```
