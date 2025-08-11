# JIRA-003: UI Bug - Serial Run Executes as Parallel from UI

**Summary:**
When selecting 'Serial' execution type from the UI, tests still run in parallel. This is fixed for console runs but not for UI-triggered runs.

**Steps to Reproduce:**
1. From the Streamlit UI, select Execution Type: Serial.
2. Run the tests.
3. Observe multiple browsers running in parallel.

**Expected Result:**
Only one browser instance should run at a time.

**Actual Result:**
Multiple browsers run in parallel.

**Evidence:**
- Screenshot: ![A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png](A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png)
- UI: Test Selection and Configuration section

**Traceability:**
- This markdown file is stored in the bug's subfolder with evidence.

---

*Attach additional evidence as needed.*
