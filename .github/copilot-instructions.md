# Copilot Instructions — MASTER_QA_SUITE (v1 line guide)

**Single Source of Truth:** Read `docs/CONTEXT_BOOTSTRAP_4444.md` first.  
This file is only a *quick index + rules* so you don’t drown in context.

---

## 0) What this repo is
Dual-engine QA framework (Selenium + Playwright) with CI, docs sync, and a Task Prioritizer. Teaches by example and runs fast in parallel.

**Key docs**
- Big context: `docs/CONTEXT_BOOTSTRAP_4444.md`
- System map: `docs/SYSTEM_MAP.md`
- Demo script: `docs/DEMO_GUIDE.md`
- Release flow: `docs/RELEASE_PROCESS.md`
- Architecture: `ARCHITECTURE.md`
- Wiki (generated): `docs/wiki/`

---

## 1) How to run locally
- Create venv, install locked deps (choose your set):
  - Core: `pip install -r requirements.txt`
  - Or modular: `pip install -r requirements-base.txt -r requirements-ui.txt -r requirements-visual.txt` (etc.)
- Run tests:
  - Selenium: `pytest -m ui -n auto --engine=selenium`
  - Playwright: `pytest -m ui --engine=playwright --browser=chromium`
  - All: `pytest -n auto`
- Streamlit runner: `streamlit run ui_streamlit/app.py`

Artifacts: `artifacts/` and `reports/` (HTML + screenshots).

---

## 2) CI/CD rules (GitHub Actions)
- Workflow: `.github/workflows/tests.yml`
- Always installs Playwright browsers; runs both engines in parallel.
- Every merge to `main` => **release tag** (vX.Y.Z or rc).
- Upload reports & screenshots as artifacts; fail fast on red.

---

## 3) Project conventions
- Tests: `tests/**` with pytest markers: `@ui @api @integration @a11y @perf @auth @security`
- Page Objects: `pages/**`
- Utilities: `utils/**` (e.g., `flaky_guard.py`, `selenium_guard.py`, `api_client.py`)
- Docs sync tool: `tools/sync_docs.py` (parses test docstrings → `docs/wiki/` + Traceability Matrix)
- Task Prioritizer CLI: `tools/task_prioritizer.py`
  - Example: `python tools/task_prioritizer.py --strategy wsjf --mark-done "Foo"`

Commit style: Conventional Commits (e.g., `feat(ui): add live logs`).

---

## 4) Copilot: do / don’t
**Do**
- Respect engine toggle (`--engine=selenium|playwright`) and markers.
- Reuse helpers in `utils/` and base classes in `pages/`.
- Put new env/config under `config/` and document in README + `RELEASE_PROCESS.md`.
- Add docstrings to tests; run `tools/sync_docs.py` after adding/renaming tests.

**Don’t**
- Don’t hardcode credentials/URLs; use `config/*.yml` or env.
- Don’t introduce new global deps without updating the right `requirements-*.in` and recompiling locks.
- Don’t rename core files (`conftest.py`, `pages/base_page.py`, `tools/task_prioritizer.py`) without updating imports + docs.

---

## 5) Where to look first (examples)
- Selenium login flow: `tests/ui/test_14_e2e_checkout_sauce.py` + `pages/sauce_login_page.py`
- Playwright sanity: `tests/playwright/test_example.py`
- A11y smoke: `tests/a11y/test_axe_home_and_cart.py`
- API schema: `tests/api/test_01_get_post_schema.py`
- Perf smoke: `tests/perf/test_nav_timing_budget.py`

---

## 6) Context discipline (to avoid 413s)
- Chunk requests: reference *paths* and *section names* (e.g., “see §Streamlit Runner in ARCHITECTURE.md”) instead of pasting large blobs.
- Prefer diffs/patches over full file rewrites.
- If you need big-picture guidance, ask for a **summary** of `docs/CONTEXT_BOOTSTRAP_4444.md` sections, not the whole file.

---

## 7) Powered By
See README “Powered By” for full credits (Selenium, Playwright, Pytest, Streamlit, Allure, Applitools*, Saucelabs*, etc.).  
\* optional/standby features—keep imports guarded.

---

## 8) When adding features
1) Write/extend tests under `tests/**` with markers + docstrings.  
2) Reuse guards (`flaky_guard`, wait utils) to minimize flake.  
3) Update docs: run `tools/sync_docs.py`.  
4) Ensure CI green, then tag release.

> If in doubt, mirror an existing pattern before inventing a new one.
