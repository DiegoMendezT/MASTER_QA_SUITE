# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: DEMO_GUIDE.md
# Purpose: Demo script and guide for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# Demo Guide

**Date:** 2025-08-10 13:45 UTC

## 5-Minute Demo Script

### 1. Switch Engines in Streamlit
- Launch the Streamlit dashboard:
  ```bash
  streamlit run ui/controls.py
  ```
- Open `http://localhost:8501` in your browser.
- Toggle between Selenium and Playwright engines.

### 2. Run a UI Test
- Execute a test using the selected engine:
  ```bash
  pytest -m "ui and not external" --engine selenium -n 4
  ```
- Show live logs and artifacts in the `reports/` directory.

### 3. Show Traceability Matrix and Wiki Sync
- Generate documentation from test files:
  ```bash
  python tools/sync_docs.py
  ```
- Highlight the auto-synced wiki in `docs/wiki`.

### 4. Mention Applitools Standby
- Explain that visual testing is marked as `@pytest.mark.visual` and excluded during the freeze.
- Show how to enable Applitools integration in future releases.

## Notes
- CI installs Playwright browsers via `python -m playwright install --with-deps`.
- Visual tests are excluded in CI during freeze: `-m "not visual"`.
