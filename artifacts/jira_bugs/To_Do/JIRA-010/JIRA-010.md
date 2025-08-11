
# JIRA-010: Network URL Not Clearly Shown in UI

**Type:** UI Bug
**Status:** To Do
**Priority:** Medium
**Reported:** 2025-08-10

## Description
The UI displays a verbose and repeated message about the Network URL for mobile/remote access. This is confusing and not intuitive. The Network URL should be clearly visible, with minimal static instructions. Guidance should be provided by an automated tutorial overlay instead of static text.

## Steps to Reproduce
1. Open the MASTER QA SUITE Test Runner in a browser.
2. Observe the Network URL section and the repeated/verbose note below it.

## Expected Behavior
- The Network URL is clearly visible.
- Only a short, intuitive message is shown.
- Tutorial overlay provides further guidance.

## Actual Behavior
- The same note about network access is repeated and verbose.
- UI is cluttered and not intuitive.

## Evidence
See attached screenshot: `A-20250810-2236_network_url_repeated.png`

## Acceptance Criteria
- Only one, short message is shown under the Network URL.
- Tutorial overlay is planned for further guidance.
- No repeated or verbose static notes.

---

**Attachments:**
- A-20250810-2236_network_url_repeated.png
