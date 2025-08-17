# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: SYSTEM_MAP.md
# Purpose: System map and subsystem overview for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# System Map

**Date:** 2025-08-10 13:45 UTC

## Subsystems Overview

### 1. Test Packs
- Located in `tests/`
- Includes UI, API, and performance tests.

### 2. Page Objects
- Located in `pages/`
- Implements the Page Object Model (POM) for maintainable UI automation.

### 3. Utilities
- Located in `utils/`
- Includes wrappers like `flaky_guard.py` and `selenium_guard.py` for retries and error handling.

### 4. Streamlit UI
- Located in `ui_streamlit/app.py`
- Provides an interactive dashboard for test execution.

### 5. Tools
- Located in `tools/`
- Includes `task_prioritizer.py` for scoring and prioritization.
- Includes `sync_docs.py` for auto-generating documentation.

## Execution Flow
Refer to the architecture diagram in `README.md` for a high-level overview of how subsystems interact.
