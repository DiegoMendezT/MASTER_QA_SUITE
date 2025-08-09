# MASTER_QA_SUITE

[![CI](https://github.com/DiegoMendezT/MASTER_QA_SUITE/actions/workflows/ci.yml/badge.svg)](https://github.com/DiegoMendezT/MASTER_QA_SUITE/actions/workflows/ci.yml)

> *"The first automation framework that tests itself as rigorously as it tests your applications."*

**What if your test framework could think, learn, and evolve?** 

MASTER QA SUITE v2.5 isn't just another Selenium automation framework—it's a **self-aware system** that combines professional-grade testing capabilities with consciousness-level self-reflection. Built for QA engineers who want their tools to be as intelligent as they are.

## 🌟 Why This Framework Is Different

### 🔄 **Self-Reflection Capabilities**
- **Tests its own structure** and validates framework integrity
- **Tracks its own evolution** through consciousness logging  
- **Measures its own effectiveness** with built-in health metrics
- **Maintains its own quality** through meta-layer validation

### ⚡ **Professional Testing Power**
- **Cross-Browser Testing**: Chrome, Firefox, Edge support with WebDriver management
- **Advanced Page Objects**: Intelligent inheritance with fallback locator patterns
- **Real-World Test Scenarios**: Login flows, form handling, dynamic content
- **Parallel Execution**: pytest-xdist integration for speed
- **Smart Data Generation**: Faker integration for realistic test data
- **Professional Reporting**: HTML reports with failure screenshots and metrics

### 🎯 **Built for Cloning & Extension**
- **Template-Ready**: Clone and adapt for any client project in minutes
- **Modular Architecture**: Add/remove components without breaking the system  
- **Configuration-Driven**: YAML-based settings for easy environment management
- **Documentation-Rich**: Every component explained and extensible

## 📁 Project Structure

```
MASTER_QA_SUITE/
├── tests/                 # Test cases and test suites
├── pages/                 # Page Object Model classes
├── drivers/               # WebDriver factory and management
├── utils/                 # Helper utilities and data generators
├── config/                # Configuration files (YAML)
├── reports/               # Test reports and failure screenshots
├── streamlit_ui/          # Web UI for test management
├── conftest.py            # Pytest fixtures and configuration
├── pytest.ini            # Pytest settings and markers
└── requirements.txt       # Python dependencies
```

## 🛠️ Setup

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd MASTER_QA_SUITE
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Running Tests

### Command Line (pytest)

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_google.py -v

# Run with markers
python -m pytest -m smoke -v

# Parallel execution
python -m pytest tests/ -n auto -v

# Generate HTML report
python -m pytest tests/ --html=reports/report.html --self-contained-html
```

### Streamlit UI

```bash
# Launch test dashboard
streamlit run streamlit_ui/app.py
```

Then open `http://localhost:8501` in your browser.

## 📊 Test Markers

- `smoke`: Critical functionality tests
- `regression`: Full regression test suite  
- `ui`: User interface tests
- `slow`: Long-running tests

## 🌐 Browser Configuration

Edit `config/settings.yaml` to customize:

```yaml
browsers:
  chrome:
    headless: false
    window_size: "1920,1080"
  firefox:
    headless: false  
    window_size: "1920,1080"
```

## ☁️ Cloud Testing (SauceLabs)

Configure `config/saucelabs_config.yaml` with your credentials:

```yaml
saucelabs:
  username: "${SAUCE_USERNAME}"
  access_key: "${SAUCE_ACCESS_KEY}"
```

## 📈 Reports

- **HTML Reports**: `reports/report.html`
- **Screenshots**: `reports/screenshots/` (on test failures)
- **Logs**: Console output with timestamp and level

## 🔧 Development

### Adding New Tests
1. Create test file in `tests/` directory
2. Import `BasePage` and create page objects in `pages/`
3. Use appropriate pytest markers
4. Follow Page Object Model patterns

### Adding New Pages
1. Create page class in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class attributes
4. Implement page-specific methods

## 🚀 CI/CD

Ready for GitHub Actions integration. Pipeline configuration supports:
- Multi-browser testing
- Parallel execution
- Test reporting
- Artifact collection

## 🏆 Portfolio Value

This framework demonstrates:
- **SDET Expertise**: Advanced Selenium patterns and best practices
- **Clean Architecture**: Page Object Model with inheritance
- **Modern Tools**: Python 3.11, pytest, Streamlit integration
- **Scalability**: Parallel execution and cloud readiness
- **Professional Quality**: Comprehensive reporting and error handling

## 📞 Support

Built with ❤️ for QA automation excellence.

---

**MASTER QA SUITE v2.0** - Showcasing 2025-level SDET capabilities
