# MASTER_QA_SUITE Roadmap

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
