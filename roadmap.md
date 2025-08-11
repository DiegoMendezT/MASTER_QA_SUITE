## Triaged Roadmap (Low Risk, High Reward First)
1. Commit message rule: Disallow '||' in commit messages (low risk, high reward for repo health)
2. Timestamp format: Change to dd-MM-yyyy_HH-mm (low risk, high reward for clarity)
3. UI: Collapsible hamburger for evidence images (low risk, high reward for UX)
4. Jira ticket UI link: Update when export is supported (low risk, medium reward)
5. Browser UX: Run test browsers minimized/behind IDE (medium risk, high reward for workflow)
6. Backlog folder tree: Create structure for backlog features (low risk, medium reward)
7. Roadmap triage: Continue to iterate and test for data safety (ongoing)
8. Kintsugi: Retrospective improvement after bugs are DONE (medium risk, high reward)
9. Machine Learning: Rename 'Consciousness' tests to 'Machine Learning' (low risk, medium reward)
10. CI/CD: Fix all workflows and keep main branch green (medium risk, high reward)
11. Jira bugs: Fix To Do bugs in order of impact/priority (medium risk, high reward)
# MASTER_QA_SUITE Roadmap

## Backlog & Notes (2025-08-10)
- Safety: Full snapshot branch exists, all cleanup is reversible, and only generated files are ignored. Manual evidence should be moved to docs/evidence/ if it must be tracked.
- UI: Test Evidence & Bug Traceability images are in a collapsible hamburger menu. Add roadmap item to update Jira ticket UI link once export is supported.
- Commit Rule: Do not allow commit messages containing '||' (not supported ASCII). Add logic/rule or backlog.
- Timestamp Format: Change all timestamps to dd-MM-yyyy_HH-mm (from yyyyMMdd-HHmm). Add to roadmap.
- Browser UX: Add feature to run test browsers minimized or behind VS Code window on Windows 11. If easy, implement now; if not, backlog for after To Do bugs are fixed.
- Roadmap: Triage roadmap items by low risk/high reward. Iterate and test for data safety.
- Backlog: Create folder tree for backlog features and logic.

## Kintsugi Note
After bugs are moved to DONE, apply Kintsugi: perform retrospective improvement and document lessons learned to strengthen the system.

## Features & Improvements
- Dual-engine (Selenium/Playwright) support
- CI/CD integration
- Docs sync and traceability
- Task Prioritizer CLI
- Streamlit UI runner
- Visual regression (Applitools)
- Performance & a11y testing
- **Bug tracking and system memory:**
  - All bugs reported are logged to `system_memory/bug_reports.md` with:
    - Unique bug ID
    - Title, evidence, URLs, reporter
    - SDLC status (Open, Fixed, Closed, etc.)
    - Dependencies (code, UI, config, etc.)
    - Traceability to test cases, UI, or code
    - Timestamps for report and closure
    - Closed bugs are retained for audit/traceability
  - System will track, timestamp, and update bug status for traceability
  - UI and CLI will provide bug reporting and review features

## See also:
- `system_memory/bug_reports.md` for current/archived bugs
- `docs/CONTEXT_BOOTSTRAP_4444.md` for context discipline
