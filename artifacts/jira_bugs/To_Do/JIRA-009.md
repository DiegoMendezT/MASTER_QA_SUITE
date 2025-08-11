# JIRA-009: Feature - Run Browsers Embedded in VS Code (Headless/Panel Mode)

**Summary:**
Browsers launched by the test suite currently open as separate windows on top of VS Code. For a more integrated developer/QA experience, allow browsers to run embedded within VS Code (e.g., in a panel, tab, or using the Simple Browser extension) as a rule, or at least as a toggle.

**Acceptance Criteria:**
- Browsers can be launched in a way that they are viewable inside VS Code (not as external windows).
- Option to toggle between embedded and external browser mode.
- Document the rule and update the README and relevant docs.
- If not feasible for all engines, document limitations and provide best effort for Playwright/Selenium.

**Rationale:**
- Improves workflow for debugging, demo, and CI visibility.
- Reduces window clutter and context switching.

**Traceability:**
- User request 2025-08-10.
- See also: conftest.py, Streamlit UI, VS Code Simple Browser extension.

---

*Attach additional evidence or implementation notes as needed.*
