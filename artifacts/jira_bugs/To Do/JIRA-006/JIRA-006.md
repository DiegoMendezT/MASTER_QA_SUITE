# JIRA-006: Bug - Missing Screenshot Evidence in Jira Bug Folders

**Summary:**
No Jira bug folder currently contains screenshot evidence, even though screenshots are generated and stored elsewhere. This breaks traceability and evidence requirements for bug tickets.

**Steps to Reproduce:**
1. Trigger a test failure that should generate a Jira bug.
2. Observe that the corresponding `artifacts/jira_bugs/JIRA-XXX/` folder contains only the markdown ticket, but no screenshot evidence.

**Expected Result:**
Each Jira bug folder should contain at least one relevant screenshot as evidence, named and timestamped according to the test failure.

**Actual Result:**
No images are present in any Jira bug folder.

**Impact:**
- Loss of traceability between bugs and visual evidence.
- QA and audit processes are hindered.

**Evidence:**
![A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png](A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png)

---

**Suggested Fix:**
Update the bug creation logic to always copy or move the relevant screenshot(s) into the Jira bug folder at creation time, and reference them in the markdown ticket.
