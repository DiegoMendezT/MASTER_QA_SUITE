# JIRA-007: Major Bug - Test Entry Point Unification & UI Regression

**Summary:**
The new test execution UI is confusing and limited compared to the previous version. The old UI, which had three selectors and a clear "Run Tests" button, provided a better user experience. The recent change removed this in favor of a less functional interface. The entry point for the old testing UI was deleted, breaking expected workflows.

**Steps to Reproduce:**
1. Open the current Streamlit launcher UI.
2. Attempt to select and run tests as before.
3. Notice the lack of flexibility and clarity compared to the previous UI.

**Expected Result:**
- The UI should provide clear, flexible test selection (as in the old UI with three selectors and a Run Tests button).
- Only one test execution entry point should exist, but it should be the more powerful and user-friendly one.

**Actual Result:**
- The new UI is limited and confusing.
- The old, better UI is no longer accessible.

**Impact:**
- Reduced usability for QA engineers.
- Loss of advanced test selection and execution options.

**Evidence:**
![A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png](A-20250810_162347_chromium_test_02_locators_and_clicks_ui_bug_failed.png)

---

**Suggested Fix:**
- Roll back the recent UI changes that removed the old test entry point.
- Integrate the old UI (with three selectors and Run Tests button) as the unified test execution entry point.
- Ensure only one entry point exists, but it must be the more functional one.
