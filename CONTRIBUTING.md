# Conventional Commits
- Use conventional commits for all changes: feat:, fix:, test:, ci:, docs:, chore:

# Local Development
- Run locally: `pytest -m "ui and not external" -n auto`

# Secrets
- Do not commit secrets. Use `.env` for local development.

### Pull Request Checklist (Task Prioritizer Protocol)

Before submitting a PR, please ensure the following:

- [ ] The PR description references the **Origin Seal** (`/docs/protocol_seal.txt`).
- [ ] The proposal includes sections for **Impact**, **Complexity**, and **Evidence**.
- [ ] At least one **divergent option** was considered and documented.
- [ ] All new code is covered by tests and appropriate markers.
- [ ] The CI/CD pipeline is green.
- [ ] You have run `python tools/sync_docs.py` and included the updated documentation in your commit.

### Engine choice
Please declare which engine you used when posting failure logs:
- Selenium: include driver caps, headless flag, and OS.
- Playwright: include `--browser` + `--headed` (if used), and OS.

### Test placement
- Selenium UI tests → `tests/ui/`
- Playwright UI tests → `tests/playwright/`
```
