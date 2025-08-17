# Roadmap: Automated UI Tutorial & Demo Runner

## Feature: Automated Selenium Tutorial & Demo for MASTER QA SUITE UI

### Description
Enable an automated Selenium-based test that runs over the Streamlit UI itself, demonstrating features and workflows. This will:
- Provide a guided tutorial with step-by-step stops (user can continue at each step).
- Offer a demo mode for each major feature (e.g., test selection, evidence viewing, bug logging).
- Add UI buttons in Streamlit to trigger these automated runs (Tutorial, Demo, Custom Run).
- Allow users to select run types and options via the UI selectors.
- Run the tests and display results directly in the Streamlit interface.

### Benefits
- New users and stakeholders can see a live, interactive walkthrough of the system.
- QA can validate the UI and workflows automatically, reducing manual effort.
- Demos and tutorials are always up-to-date with the current UI.

### Acceptance Criteria
- [ ] Selenium script can launch and interact with the Streamlit UI, following a defined tutorial path.
- [ ] Tutorial mode pauses at key steps, waiting for user input to continue.
- [ ] Demo mode runs through features without stopping.
- [ ] Streamlit UI has buttons to trigger Tutorial, Demo, and Custom runs.
- [ ] Test results and progress are shown in the UI.
- [ ] All selectors and run options are available for automated runs.

---

*Added to roadmap on 2025-08-10 by request.*
