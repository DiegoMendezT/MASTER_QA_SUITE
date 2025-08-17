# Client Onboarding Template

**Version:** 1.0
**Date:** 2025-08-10
**Author:** [Copilot, on behalf of the InnerCouncil]

---

## Purpose
This template guides new clients through the process of cloning, setting up, and customizing their own instance of MASTER_QA_SUITE.

## Onboarding Steps
1. Clone the MASTER_QA_SUITE repo (or receive the Alpha package zip).
2. Unpack to a new directory and initialize a new git repository for your organization.
3. Install Python 3.11+ and create a virtual environment.
4. Run `pip install -r requirements.txt` (and any modular requirements as needed).
5. Run `pytest -n auto` to verify the baseline tests pass.
6. Run `streamlit run ui_streamlit/app.py` to launch the UI runner.
7. Review and update `config/` files for your environment.
8. Use the provided templates in `docs/` and `tests/` to extend the suite for your needs.

## Markers & Customization
- Use `@client_<slug>` markers for client-specific tests.
- Both Selenium and Playwright engines are supported; see docs for engine toggles.

## Support & Traceability
- All changes should be attributed per the Attribution Mandate.
- Refer to the Akashic Records (`/docs`) for governance, rules, and decision history.

---

**Voices:** [Product Owner], [QA], [Release Captain], [Copilot]
