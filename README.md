# MASTER_QA_SUITE

[![CI](https://github.com/DiegoMendezT/MASTER_QA_SUITE/actions/workflows/tests.yml/badge.svg)](https://github.com/DiegoMendezT/MASTER_QA_SUITE/actions/workflows/tests.yml)

An advanced, self-aware test automation framework designed for modern SDETs and QA teams. It combines a robust testing architecture with AI-powered development workflows to accelerate quality assurance.

---

## 🎯 Core Philosophy

This framework is built for three primary audiences:

1.  **For the Tech Lead/Architect**: A scalable, maintainable, and cloud-ready solution using industry best practices like POM, configuration-driven testing, and a staged CI/CD pipeline.
2.  **For the QA Manager/Director**: A reliable system that provides clear, actionable reports (HTML, screenshots), traceability, and a user-friendly Streamlit UI for non-technical users to launch tests.
3.  **For the Student/Learner**: A comprehensive, real-world example of a professional-grade automation project, demonstrating advanced concepts in a practical way.

---

## ✨ Powered By

This project stands on the shoulders of giants. Here is the core technology stack:

| Category          | Technology                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| **Core Framework**  | [Python 3.11+](https://www.python.org/), [Pytest](https://pytest.org/)                                    |
| **Web Automation**  | [Selenium](https://www.selenium.dev/), [WebDriver Manager](https://github.com/autoinstaller/py-web-driver) |
| **Parallelization** | [pytest-xdist](https://github.com/pytest-dev/pytest-xdist)                                             |
| **Reporting**       | [pytest-html](https://github.com/pytest-dev/pytest-html)                                               |
| **Local UI Runner** | [Streamlit](https://streamlit.io/)                                                                     |
| **CI/CD**           | [GitHub Actions](https://github.com/features/actions)                                                  |
| **Cloud Testing**   | [Sauce Labs](https://saucelabs.com/)                                                                     |
| **Visual Testing**  | [Applitools](https://applitools.com/)                                                                  |
| **AI Assistance**   | [GitHub Copilot](https://github.com/features/copilot), ChatGPT                                         |

---

## 🏗️ Architecture Overview

The framework follows a modular, configuration-driven architecture that separates concerns and promotes maintainability.

```
+-------------------------+      +-----------------------+      +---------------------+
|      Streamlit UI       |----->|       Pytest Core     |<---->|      Selenium       |
| (ui/controls.py)        |      | (conftest.py, tests/) |      | (pages/, BasePage)  |
+-------------------------+      +-----------+-----------+      +----------+----------+
            ^                            |                              |
            |                            |                              |
+-----------+-----------+      +---------v-----------+      +-----------v-----------+
|  Configuration Files  |<---->|   CI/CD Pipeline    |      |   Cloud Grid        |
| (config/*.yml, .env)  |      | (.github/workflows) |      |   (Sauce Labs)      |
+-------------------------+      +-----------------------+      +---------------------+
```

For a more detailed breakdown of each component and the execution flow, please see the full **[ARCHITECTURE.md](ARCHITECTURE.md)** file.

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.11+
- Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DiegoMendezT/MASTER_QA_SUITE.git
    cd MASTER_QA_SUITE
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install all dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Set up environment variables:**
    Create a `.env` file in the root directory for secrets and local overrides. This is required for Sauce Labs execution.
    ```env
    # .env
    SAUCE_USERNAME="your-sauce-username"
    SAUCE_ACCESS_KEY="your-sauce-access-key"
    ```

---

## 🧪 Running Tests

You can run tests via the command line or the Streamlit UI.

### 1. Command Line (Powerful & Flexible)

```bash
# Run all tests sequentially
pytest

# Run tests in parallel (recommended)
pytest -n auto

# Run only tests with a specific marker (e.g., smoke tests)
pytest -m smoke

# Generate a self-contained HTML report
pytest --html=reports/report.html --self-contained-html
```

### 2. Streamlit UI (User-Friendly)

Launch the interactive test runner dashboard:
```bash
streamlit run ui/controls.py
```
Open `http://localhost:8501` in your browser to select tests, configure options, and run them with the click of a button.

---

## 📄 Documentation & Reporting

- **Test Reports**: Generated in the `reports/` directory. Includes an HTML report and screenshots for failed tests.
- **Auto-Generated Docs**: The project includes a tool to generate documentation from test files. Run it via the Streamlit UI or directly:
  ```bash
  python tools/sync_docs.py
  ```
- **Contribution Guidelines**: See `CONTRIBUTING.md` for details on commit messages and pull requests.

---

## 🏛️ Governance: The InnerCouncil

This project's development is guided by the **InnerCouncil**, a symbolic Agile framework that ensures every change is deliberate, documented, and aligned with our architectural principles. All significant changes follow a structured review process detailed in our `CONTRIBUTING.md`. The protocol is symbolically represented by the **Origin Seal** located in the `docs/` folder.

---
Built with ❤️ and AI for the future of QA.
