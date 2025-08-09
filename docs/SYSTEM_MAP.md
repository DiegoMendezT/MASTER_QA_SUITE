# System Map

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
