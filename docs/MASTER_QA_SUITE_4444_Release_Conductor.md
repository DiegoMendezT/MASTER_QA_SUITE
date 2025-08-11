# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: MASTER_QA_SUITE_4444_Release_Conductor.md
# Purpose: Master summary, index, and roadmap for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# MASTER_QA_SUITE — 4444-Word Master Summary, Index & Roadmap (Release Conductor)

**Date:** 2025-08-10 13:45 UTC
**Mode:** Freeze-safe (hotfixes only).
**Prime mission:** Turn CI green on `main`, tag `v1.0.1`, keep demos smooth, keep docs true, preserve reversibility.

---
## Executive Snapshot
MASTER_QA_SUITE is a dual-engine test framework (**Selenium** + **Playwright**) under **pytest** with **xdist** parallelism, a **Streamlit** runner for local control, and a documentation engine that turns test docstrings into a living wiki and a **Traceability Matrix**. Governance is handled by **`tools/task_prioritizer.py`** (formerly InnerCouncil) to ensure we always pick the smallest, most valuable next step. We operate under a **freeze**: only hotfixes and CI/doc stability work ship until we tag a clean patch release.

## Master Index (what to read and why)
1. **Diego × Working Agreement** — who, why, constraints, pressure points.
2. **Architecture** — engines, layers, fixtures, guards, artifacts.
3. **Conventions** — flags, markers, structure, naming canon.
4. **CI/CD** — workflow anatomy, artifacts, secrets policy, release gates.
5. **Docs & Demo** — wiki sync, demo script, “Powered By”.
6. **Client Drop-In** — clone for a new site without touching kernel.
7. **Break-Glass Triage** — 3 steps to green CI.
8. **Roadmap** — Now / Next / Later with acceptance criteria.
9. **Risk & Guardrails** — the four gates + 4o safety.
10. **Golden Commands** — local/CI recipes, tag/rollback.

## Diego, Intent, and Working Agreement (short)
- **Who:** Diego Alejandro Méndez Trejos (QA/SDET, CR). Systems thinker. Builds frameworks that **teach while they test**.
- **Intent:** A stable, demo-ready, cloneable baseline; frequent small releases; clean rollbacks; documentation that stays true.
- **Constraints:** Freeze; no features; only surgical hotfixes.
- **Pressure points:** Time, energy, and income → bias to boring reliability; 4o/413 issues → chunked context; low tolerance for flake.
- **Implications:** We move in **small diffs**; we ship only on green; we leave artifacts and decision logs.
- **Agreement:** Act → Verify → Document → Rollback notes. Ask only if blocked by secrets/URLs/org policy.

## System Architecture (concise, source-of-truth)
- **Engines:**
  - Selenium (primary): hardened browser profile, robust click via JS fallback, cloud-ready (Sauce Labs).
  - Playwright (secondary): fast, headless-first; owns `--browser/--headed/--headless` flags.
  - Selection: `--engine=selenium|playwright`; Selenium browser via **`--selenium-browser`**.
- **Layers & key files:**
  - `tests/` with suites (`ui`, `api`, `integration`, `perf`, `a11y`, `visual`, `playwright`).
  - `pages/` with `base_page.py` (waits + click fallback) and site pages.
  - `utils/` with `flaky_guard.py`, `selenium_guard.py`, `logger.py`.
  - `tools/` with `task_prioritizer.py`, `sync_docs.py`.
  - `ui_streamlit/app.py` and `ui/controls.py` for local UX.
  - `config/` with `settings.yaml`, `integration.yaml`, backlog/roadmap data.
  - Artifacts: `reports/report.html`, `artifacts/screenshots/**`.
- **Docs are code:** `sync_docs.py` reads test docstrings/markers → `docs/wiki/*` + `Traceability_Matrix.md`.

## Conventions that keep us out of trouble
- **Flags:** Do not redefine Playwright flags. Use **`--selenium-browser`** for Selenium.
- **Markers:** `ui, api, integration, a11y, perf, auth, security, visual, smoke, profile` (declare in `pytest.ini`).
- **Naming canon:** Task engine is `tools/task_prioritizer.py`. Do not resurrect `innercouncil.py`.
- **Artifacts:** Always write screenshots on fail; always emit an HTML report.
- **Freeze:** No new deps; no refactors that change behavior; only hotfixes and CI/doc fixes.

## CI/CD — expectations and the minimal patch we applied
- **Workflow:** `.github/workflows/tests.yml`.
- **Install from locks:** `requirements*.txt` (pip-tools compiled).
- **Browser install (Playwright legs):** `python -m playwright install --with-deps`.
- **Matrix:** at least Selenium+Chrome and Playwright+Chromium; can expand.
- **Artifacts:** upload `reports/` and `artifacts/screenshots/` for every job.
- **Secrets:** If Sauce/Applitools secrets are missing, **skip**, don’t fail.
- **Release step:** only when CI is green and a version tag is pushed.

## Docs & Demo
- **Docs:** Updated by `sync_docs.py`; traceability displayed in the wiki.
- **Demo (7 minutes):** same test on both engines, force a tiny failure to show screenshot + HTML report, run docs sync, open a generated page.
- **Powered By:** explains library choices and attribution.

## Client “Drop-In” without touching the kernel
- Create `clients/<slug>/` with pages, selectors, env overlays, and a thin `conftest.py` to merge config.
- Add markers `@client_<slug>`, `@smoke`, `@regression`.
- Tests narrate flows; Page Objects hold logic; selectors prefer `data-test` attributes.
- Dual-engine compatible; kernel remains immutable.

## Break-Glass Triage (3 steps to green)
1) **Reproduce fast:** fresh venv; install from locks; run subset with `-n auto`.
2) **Isolate the fault:** run targeted paths; check report + screenshots.
3) **Minimal fix:** marker add, Playwright install step, flag namespace, or skip secrets. Commit tiny patch; re-run CI; tag when green.

## What we finished
- Hardened Selenium profile, robust JS click, and FlakyGuard waits.
- Dual-engine selection and conventions; Playwright integrated.
- CI workflow with Playwright browser install, caches, artifacts, and tag-driven release job.
- Docs sync end-to-end and demo script.
- Client extension pattern documented.
- Golden commands and rollback playbook.

## What we’re doing now
- **Stage 0:** sanity scan (markers vs `pytest.ini`; workflow steps present).
- **Stage 1:** agree on local “paper run” commands for Selenium and Playwright.
- **Stage 2:** if CI is red, apply surgical diffs only.
- **Stage 3:** when green, tag `v1.0.1`, write notes, and publish release.
- **Stage 4:** docs sync and demo readiness pass.

## What we will do next (freeze-safe roadmap)
- **Docs parity:** ensure README/wiki reflect truth after the release.
- **Demo polish:** repeat 7-minute script reliably; Streamlit runner showcases live logs and report opening.
- **Onboard one client:** smoke + one regression path via drop-in model.
- **PR hygiene:** add a quick smoke job for PRs; keep full matrix on `main`.
- **Optional hygiene:** coverage artifact, Bandit (non-blocking), PR template and CODEOWNERS.

## Acceptance criteria
- **Now:** Green CI (both engines), artifacts uploaded, tag pushed, notes published.
- **Next:** Demo runs end-to-end on a fresh machine; client smoke green locally; docs synced.
- **Later:** Optional hygiene jobs exist and skip gracefully without secrets.

## Risk & Guardrails
- **Four gates:** 🚦 CI Green, 🚦 Docs Parity, 🚦 Reversible, 🚦 Dual-Engine Safe.
- **Flag collisions:** never redefine Playwright flags; Selenium uses **`--selenium-browser`**.
- **Marker drift:** add to `pytest.ini` when new markers appear.
- **Secrets missing:** skip cloud/visual steps; never fail the whole pipeline because of absent secrets.
- **4o safety:** chunk, avoid giant pastes, stop on loop and return max three actions.

## Golden commands (local & CI)
- **Local smoke:** `pytest -n auto --maxfail=1 -q`
- **Selenium:** `pytest -n auto --engine=selenium --selenium-browser=chrome`
- **Playwright:** `python -m playwright install --with-deps && pytest -n auto --engine=playwright --browser=chromium`
- **HTML report:** `pytest --html=reports/report.html --self-contained-html`
- **CI re-run (no-op):** `git commit --allow-empty -m "ci: retrigger" && git push`
- **Tag on green:** `git tag v1.0.1 && git push origin v1.0.1`
- **Rollback:** `git revert <sha>` or hotfix from last good tag.
