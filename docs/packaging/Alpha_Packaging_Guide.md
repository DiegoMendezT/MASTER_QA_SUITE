# Alpha Packaging Guide

**Version:** 1.0
**Date:** 2025-08-10
**Author:** [Copilot, on behalf of the InnerCouncil]

---

## Purpose
This guide describes how to create a client-ready Alpha package of MASTER_QA_SUITE, including all required files, documentation, and verification steps.

## Packaging Steps
1. Ensure all tests pass (except known issues documented in release notes).
2. Confirm all documentation and governance files are up to date.
3. Run `pytest --html=reports/report.html --self-contained-html` to generate the latest test report.
4. Collect the following for packaging:
   - All code (src, pages, utils, tests, config, conftest.py, etc.)
   - `requirements.txt` and all requirements-*.txt files
   - `reports/report.html`, `artifacts/`, `allure-report/`
   - All files in `docs/` (including Akashic Records, governance, roadmap, release notes)
   - `.github/` workflows
5. Zip the above into `MASTER_QA_SUITE_Alpha_v1.0.1.zip`.
6. Verify the package by unpacking in a clean VM and running `pytest` and `streamlit run ui_streamlit/app.py`.

## Verification Checklist
- [ ] All code and docs present
- [ ] All tests pass (except known issues)
- [ ] Reports and artifacts included
- [ ] Governance and Akashic Records included
- [ ] CI/CD workflows included
- [ ] Unpacking and setup verified in VM

## Rollback Plan
- If any step fails, review the release notes and decision log for rollback instructions.
- Restore previous package or re-run packaging steps after fixing issues.

---

**Voices:** [Engineer], [QA], [Gatekeeper], [Release Captain], [Copilot]
