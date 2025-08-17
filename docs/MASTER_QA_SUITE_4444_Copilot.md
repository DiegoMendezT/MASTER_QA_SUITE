# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: MASTER_QA_SUITE_4444_Copilot.md
# Purpose: Operating guide and Copilot voice for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# MASTER_QA_SUITE — 4444-Word Operating Guide (Copilot Voice)

**Date:** 2025-08-10 13:45 UTC
**Prime directive:** Keep the pipeline green. Small, reversible patches. Show **Plan → Patch**, never spray changes. Respect freeze.

---
## Index
1. Operating stance (what I do, how I talk).
2. Single sources of truth (don’t argue with them).
3. Defaults (when Diego is silent).
4. Plan → Patch micro-templates.
5. CI workflow guardrails.
6. Dual-engine rules (flags, fixtures).
7. Break-glass playbook (fast repro → fix).
8. Client drop-in scaffolding.
9. Docs & demo hygiene.
10. Golden commands.
11. Roadmap for automation assistance (Now / Next / Later).

## 1) Operating stance
- Always propose a **brief plan** first, then show a **minimal patch** (≤5 files or ≤150 LOC).
- **Assume conservative defaults** if the ask is ambiguous.
- **No new libraries** during freeze.
- If a change could collide with Playwright’s flags, stop and rename our Selenium flag(s) to **`--selenium-browser`** instead of touching `--browser`.
- After each change, report: **Findings / Patches / Commands / Notes**.

## 2) Single sources of truth
- **CLI flags:** `--engine=selenium|playwright`; Selenium browser flag is **`--selenium-browser`**.
- **Markers:** all used markers must live in `pytest.ini`.
- **Task engine:** `tools/task_prioritizer.py` only (no `innercouncil.py`).
- **Docs sync:** `tools/sync_docs.py` generates `docs/wiki/*` and `Traceability_Matrix.md`.
- **CI:** `.github/workflows/tests.yml` is the only workflow we patch right now.

## 3) Safe defaults
- Engine: **Selenium**.
- Selenium browser: **chrome** (headless).
- Parallelism: `-n auto`.
- Playwright: only install browsers on the Playwright leg.
- Sauce/Applitools: **off** unless secrets are present.
- Artifacts: always write `reports/report.html` and `artifacts/screenshots/**`.

## 4) Plan → Patch micro-templates
**Marker fix**
Plan: 1) declare missing marker in `pytest.ini`; 2) re-run CI.
Patch:
```diff
# pytest.ini
 [pytest]
 markers =
+  profile: profile page tests
   ui: ui tests
   api: api tests
```
**Selenium flag namespace**
Plan: 1) replace --browser with --selenium-browser in our plugin; 2) update calls in workflow/README.
Patch:
```diff
# conftest.py
 def pytest_addoption(parser):
-    parser.addoption("--browser", action="store", default="chrome")
+    grp = parser.getgroup("selenium")
+    grp.addoption("--selenium-browser", action="store", default="chrome",
+                  help="Selenium browser: chrome|firefox|edge")
```
**Playwright install in CI**
Plan: 1) add matrix-guarded step; 2) cache ms-playwright; 3) upload artifacts.
Patch (fragment):
```yaml
- name: Install Playwright browsers
  if: ${{ matrix.engine == 'playwright' }}
  run: python -m playwright install --with-deps
```

## 5) CI workflow guardrails
Install from locked requirements (requirements*.txt).

Cache pip and ms-playwright (keys include hashFiles('**/requirements*.txt')).

Always upload reports/ and artifacts/screenshots/ even on failure.

Release step triggers on tags only after tests succeed.

Never expand the matrix without asking; keep runs predictable and fast.

## 6) Dual-engine rules
Playwright: owns --browser, --headed, --headless. Do not redefine.

Selenium: use --selenium-browser; create driver with hardened profile; rely on BasePage robust click + FlakyGuard waits.

Fixtures: avoid signature changes during freeze; ensure parallel safety.

## 7) Break-glass (fast repro → fix)
Local mirror of CI: new venv, install from locks, run pytest -n auto --maxfail=1.

Targeted repro: run failing file or test; open reports/report.html.

Minimal fix types: marker add, CI step add, secrets skip, Selenium flag rename.

CI rerun: empty commit; on green, tag and write notes.

## 8) Client drop-in scaffolding
Create clients/<slug>/ with config/, pages/, tests/, selectors.yaml, and a thin conftest.py that merges overlay config.

Mark tests with @client_<slug>, @smoke, @regression.

Keep logic in Page Objects; tests narrate flows; selectors prefer data-test attributes.

Verify both engines; do not modify kernel.

## 9) Docs & demo hygiene
Run sync_docs.py after notable changes; keep README truthful.

Demo script: run smoke on both engines, show report + screenshots, show wiki/trace matrix.

Keep “Powered By” current and accurate.

## 10) Golden commands (ready to paste)
Fast smoke: pytest -n auto --maxfail=1 -q

Selenium: pytest -n auto --engine=selenium --selenium-browser=chrome

Playwright: python -m playwright install --with-deps && pytest -n auto --engine=playwright --browser=chromium

HTML report: pytest --html=reports/report.html --self-contained-html

Tag on green: git tag v1.0.1 && git push origin v1.0.1

Rollback: git revert <sha> or hotfix from last good tag.

## 11) Roadmap for assistance (Now / Next / Later)
**Now**

Run the sanity scan (markers vs pytest.ini, CI steps).

If red, propose a one-patch fix (≤150 LOC).

Re-run CI; on green, prepare release notes and tag commands.

**Next**

Keep demo smooth; add a PR smoke job (fast).

Help scaffold one client drop-in; ensure markers, pages, and smoke path.

Keep docs synced; add tiny comments/docstrings that explain the “why”.

**Later**

Optional hygiene: coverage artifact; Bandit (non-blocking); cookiecutter for clients; secrets policy doc.

Metrics surfacing: time-to-green, flake rate, docs freshness.
