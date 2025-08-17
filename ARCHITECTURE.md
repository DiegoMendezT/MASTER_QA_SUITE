# MASTER_QA_SUITE Architecture

This document provides a detailed overview of the architecture of the MASTER_QA_SUITE automation framework.

## Core Principles

The framework is built on the following core principles:
- **Modularity**: Components are designed to be independent and interchangeable.
- **Scalability**: The architecture supports parallel execution and cloud integration.
- **Maintainability**: Code is written to be clean, readable, and easy to maintain, following the Page Object Model (POM).
- **Configuration over Code**: Behavior is controlled through external configuration files (`.yml`) rather than hard-coded values.

## Directory Structure

```
MASTER_QA_SUITE/
├── .github/              # GitHub Actions workflows and templates
├── .venv/                # Python virtual environment
├── config/               # Environment and test configuration (YAML)
├── docs/                 # Auto-generated test documentation
├── pages/                # Page Object Model (POM) classes
├── reports/              # Test reports and failure screenshots
├── tests/                # Pytest test cases
├── tools/                # Helper scripts, e.g., documentation generator
├── ui/                   # Streamlit UI for test execution
├── .copilot/             # Configuration to enhance Copilot's context
├── .gitignore            # Git ignore file
├── ARCHITECTURE.md       # This file
├── CONTRIBUTING.md       # Contribution guidelines
├── README.md             # Project overview and setup guide
├── conftest.py           # Core pytest fixtures (e.g., WebDriver setup)
├── pytest.ini            # Pytest configuration (markers, paths)
└── requirements.txt      # Python dependencies
```

## Key Components

### 1. Test Runner (`pytest`)
- **`pytest`** is the core test execution engine.
- **`pytest-xdist`** enables parallel test execution to significantly reduce run time.
- **`pytest-html`** generates detailed HTML reports with test results.
- **Fixtures (`conftest.py`)**: Fixtures are used for setup and teardown, dependency injection (e.g., `driver` instance), and managing test context.

### 2. Web Automation (`Selenium`)
- **`Selenium WebDriver`** is used for browser automation.
- **`WebDriver Manager`** automatically handles the download and management of browser drivers (Chrome, Firefox, Edge).
- **Page Object Model (`pages/`)**: The POM design pattern is strictly followed. Each page in the application has a corresponding class that contains its elements (locators) and the methods to interact with them. This separates test logic from UI interaction logic, making tests cleaner and more maintainable.
- **`BasePage`**: A foundational class that all page objects inherit from, providing common functionalities like clicking, sending keys, and waiting for elements.

### 3. Configuration (`config/`)
- The framework is driven by YAML configuration files.
- **`settings.yml`**: Contains general settings like browser configurations, window sizes, and timeouts.
- **`saucelabs.yml`**: Holds credentials and capabilities for running tests on Sauce Labs.
- Using `.env` files for managing secrets like API keys and Sauce Labs credentials, which are loaded at runtime.

### 4. Streamlit UI (`ui/`)
- A web-based UI built with **`Streamlit`** provides an interactive dashboard for running tests.
- Users can select browsers, toggle headless mode, run tests on Sauce Labs, and specify pytest markers or test paths without using the command line.
- It provides a user-friendly interface for non-technical users to execute tests and view results.

### 5. CI/CD (`.github/workflows/`)
- **GitHub Actions** automates the testing process.
- The `tests.yml` workflow defines a multi-stage pipeline:
    1.  **Lint**: Code quality is checked with `ruff`.
    2.  **Fast Tests**: Non-UI tests are run first for quick feedback.
    3.  **UI Tests**: A matrix strategy runs the full UI test suite in parallel across multiple browsers (Chrome, Firefox, Edge) on Sauce Labs.
- Test reports and screenshots are uploaded as artifacts for easy debugging.

### 6. Documentation (`tools/sync_docs.py`)
- A custom script, `sync_docs.py`, automatically generates markdown documentation from test file docstrings and markers.
- This creates a living documentation system and a traceability matrix, ensuring that documentation is always up-to-date with the test suite.

### 7. Visual Testing (`Applitools`)
- **`Applitools Eyes`** is integrated for automated visual regression testing.
- The `eyes` fixture in `conftest.py` manages the connection to the Applitools Ultrafast Grid.
- Tests can capture screenshots of pages or elements and compare them against an established baseline, catching unintended UI changes that functional tests might miss.

## Dual-Engine Execution Model
- **Router**: The test engine is selected via the `--engine {selenium|playwright}` flag, which is also surfaced in the Streamlit UI.
- **Selenium Path**: Tests rely on the custom `driver(config, request)` fixture, which is parallel-safe and Sauce-aware.
- **Playwright Path**: Tests use `pytest-playwright`’s native fixtures (`page`, `context`, `browser`), ensuring no overlap with Selenium fixtures.
- **Isolation**: Playwright tests are located under `tests/playwright/`, while Selenium tests reside in `tests/ui/` and other directories. Both can run from the same repository and CI matrix without conflicts.
- **CI**: GitHub Actions runs Selenium jobs (either locally or on Sauce Labs) and a separate Playwright job (across chromium, firefox, and webkit).

## Execution Flow

1.  **Initialization**: `conftest.py` reads configuration files and sets up the environment based on command-line arguments or Streamlit UI selections.
2.  **Driver Fixture**: The `driver` fixture creates a thread-safe WebDriver instance (either local or remote on Sauce Labs) for each test function.
3.  **Test Execution**: `pytest` discovers and runs tests. Tests instantiate Page Objects to interact with the application.
4.  **Reporting**: After the test run, `pytest-html` generates a report, and screenshots are saved for any failing tests.
5.  **CI Trigger**: On a push or pull request to the `main` branch, the GitHub Actions workflow is triggered, executing the entire pipeline.
