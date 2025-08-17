# Engines: Selenium & Playwright

## When to use what
- **Selenium**: for full browser fidelity, a rich ecosystem, remote farms (Sauce Labs), and extensible hooks.
- **Playwright**: for speed, reliability, easy headless execution, powerful selectors, and built-in tracing.

## Quick Start
```bash
# Selenium
pytest -m "ui and not external" --engine selenium -n 4

# Playwright (headless)
pytest tests/playwright --engine playwright --browser chromium

# Playwright (headed)
pytest tests/playwright --engine playwright --browser chromium --headed
```

## Fixtures
- **Selenium**: `driver` (framework), `config` (framework).
- **Playwright**: `page`, `context`, `browser` (from `pytest-playwright`).

## Local Setup
```bash
pip install -r requirements.txt
python -m playwright install
```

## CI Notes
Linux images often require: `python -m playwright install --with-deps`.

Artifacts: HTML reports + screenshots are uploaded per job.
