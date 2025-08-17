# Symbolic Memory Log — MASTER_QA_SUITE

## Evidence Traceability & Jira Bug Automation (as of 2025-08-10)

### System Rules & State
- All Jira bug folders (JIRA-001 to JIRA-008) now contain a valid, viewable PNG evidence image named with the standardized convention: `A—<timestamp>_chromium_test_02_locators_and_clicks_ui_bug_failed.png`.
- Each Jira markdown ticket references the correct evidence file in its folder.
- When a new Jira bug is created (by user or Copilot), the next Copilot answer will prompt for evidence. Once provided, the image is saved in the Jira folder and referenced in the markdown.
- This logic is now enforced for all current and future Jira bugs.
- All old/broken/empty evidence files have been removed or replaced.
- The evidence pipeline is validated: images display in both VS Code and the Streamlit UI.

### Retroactive Fixes Completed
- JIRA-001 to JIRA-008: All markdown tickets and evidence files updated.
- All folders now have a valid PNG and correct markdown reference.
- No broken or missing evidence images remain.

### Next Steps
- For any new bug, evidence will be requested and processed automatically.
- If a bug is reported, Copilot will prompt for evidence and update the Jira folder accordingly.
- System is ready for further testing or new bug creation.

---

_Last update: 2025-08-10_
