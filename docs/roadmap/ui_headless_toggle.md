# Roadmap Item: UI Toggle for Headless Browser Option

## Summary
Add logic and UI to allow users to toggle between headless and non-headless browser mode when running tests from the UI.

## Motivation
- Improve developer experience by allowing flexible browser visibility during test runs.
- Support both CI (headless) and local debugging (headed) workflows.

## Acceptance Criteria
- UI element (checkbox, switch, or dropdown) to select headless or headed mode.
- Test runner logic reads UI state and launches browser accordingly.
- Default to headless in CI, but allow override from UI.
- All changes logged for traceability (Akashic Records).
- QA to review and approve implementation.

## Tasks
- [ ] Design UI toggle component.
- [ ] Implement toggle logic in test runner backend.
- [ ] Wire up UI to backend logic.
- [ ] Add traceability and logging for toggle state.
- [ ] QA review and sign-off.

## Accountability
- All decisions and changes to be logged in Akashic Records.
- QA and UI/UX voices to review and approve.
