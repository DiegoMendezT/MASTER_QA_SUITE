# JIRA-008: Bug - Broken Evidence Images in Jira Bug Folders

**Summary:**
Images saved as evidence in Jira bug folders (e.g., `evidence.png`, `evidenceA.png`) are not displaying correctly and appear as broken files in the UI and VS Code. This prevents visual verification of bug evidence.

**Steps to Reproduce:**
1. Trigger a bug that saves a screenshot as evidence in a Jira bug folder.
2. Open the image in VS Code or the UI.
3. Observe that the image cannot be loaded (broken image icon or error message).

**Expected Result:**
Evidence images in Jira bug folders should be viewable and valid PNG files.

**Actual Result:**
Images are broken and cannot be displayed.

**Impact:**
- Loss of visual traceability for bugs.
- QA and audit processes are hindered.

**Evidence:**
![A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png](A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png)

---

**Suggested Fix:**
- Ensure that when copying or saving evidence images to Jira bug folders, the file is a valid PNG and not an empty or corrupted file.
- Add validation after saving/copying to confirm image integrity.
