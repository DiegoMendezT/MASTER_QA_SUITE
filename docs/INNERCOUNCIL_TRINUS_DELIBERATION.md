# InnerCouncil Deliberation — Trinus Demo (MVP planning)

Date: 2025-10-24
Repo branch: `feature/trinus-demo` (scaffold committed locally)

Purpose
-------
This document records a synthetic "inner council" triage and planning conversation that mirrors Agile ceremonies (triage → grooming → plan). The goal is to produce a compact, agreed plan for the Trinus demo work, mark which actions Automation can execute, and list the exact human approvals (decisions) the council needs.

Context
-------
- We already scaffolded a minimal Streamlit Trinus demo page, a `config/clients/trinus.yaml`, and an `tools/evidence_manager.py` utility. These are committed on `feature/trinus-demo` locally.
- The system supports parallel browser workers (up to ~16) and headless/visible modes. Evidence retention and rotation are required to avoid "burned" stale artifacts.
- The project has a roadmap (`config/roadmap_phase2.yml`) with epics and tasks. We ran into a minor issue executing `tools/task_prioritizer.py` due to a small code bug (uses `field(Task)` instead of `fields(Task)`), so automatic prioritization failed. The council proceeds using the roadmap contents and human judgement while flagging that minor fix.

Council composition (synthetic voices)
-------------------------------------
- QA Director (QA): cares about stability, reproducibility, and business-facing reliability. Votes for FlakyGuard and Live Artifacts.
- Automation Engineer (AE): focuses on implementability, reuse, CI, and parallel execution. Prefers Env switcher and data factories early.
- Product Owner (PO): values ROI and demos that close deals — prefers visible artifact and demo polish (Live Artifacts, Visual Baseline).
- ML Researcher (ML): looks at learning & future value—supports tasks that build capabilities (FlakyGuard, Contract tests).
- Compliance/Security (Sec): blocks anything that stores secrets in repo; requests policies and env-based secret storage.

Round 1 — quick scoring (qualitative)
------------------------------------
All voices read the tasks from `roadmap_phase2.yml` and gave quick qualitative scores (high/medium/low). The main signals:

- T2-01 FlakyGuard: High ROI, medium complexity — improves reliability for all demos and CI stability. (QA: HIGH, AE: MED, ML: HIGH)
- T2-03 Env switcher & secrets: High ROI, low complexity — required for client demos to target Trinus staging/prod safely. (AE: HIGH, Sec: HIGH)
- T2-02 Live artifacts panel: High ROI for demos and sales — medium complexity (PO: HIGH, QA: HIGH)
- T2-04 Test data factory: Medium ROI, medium complexity — supports repeatable demos (AE: MED, ML: MED)
- T2-07 Contract tests: Medium-High ROI for hardening (PO: MED, ML: HIGH)
- T2-08 UI↔API parity checks: Medium ROI, medium complexity (QA: MED)
- T2-05 Playwright mobile matrix & T2-06 Visual Baseline: useful but can be scheduled after core stability (PO: MED, AE: LOW initially)

Consensus prioritized list (MVP ordering)
--------------------------------------
1. T2-03 — Env switcher & secrets model (essential for safe client demos)
2. T2-01 — FlakyGuard: retries + smart waits (stability foundation)
3. T2-02 — Live artifacts panel in Streamlit (demo UX + shareability)
4. T2-04 — Test data factory + fixtures (repeatability & self-test)
5. T2-07 — Contract tests + schema registry (risk reduction)
6. T2-08 — UI↔API parity checks
7. T2-05 — Playwright mobile emulation matrix (coverage)
8. T2-06 — Visual Baseline Manager
9. T2-09 / T2-10 — Docs & course enhancements (ongoing parallel work)

Rationale (short)
-----------------
- Env switcher first because demos must target the correct Trinus environment and avoid leaking credentials or writing evidence to the wrong place.
- FlakyGuard next because flaky runs make demos and CI unreliable; adding retries and auto-screenshots provides fast wins.
- Live artifacts panel gives sales and reviewers the immediate ability to inspect runs and share demos.

Automation vs Human decisions
----------------------------
Automation agent (what I can do right now):

- Create and commit scaffolds for the Live Artifacts panel (Streamlit UI hooks) — already partly done via `tools/evidence_manager.py` and `ui_streamlit/pages/trinus_demo.py`.
- Add an `--env` flag and a lightweight config resolver for demo runs (modify runner CLI) — can be implemented and tested locally.
- Implement a FlakyGuard prototype: small decorator/fixture that wraps test steps with retries and smart waits — can be added as an optional plugin/fixture.
- Wire a simple retention/prune policy for artifacts (dry-run mode) — `tools/evidence_manager.py` already includes prune logic.

Human approvals required (explicit asks for you)
---------------------------------------------
The inner council needs the following confirmations from you before automation proceeds to execute remote changes or CI runs:

1) Push approval: Push `feature/trinus-demo` to remote? (yes/no) — required to enable CI runs and backup remote state.
2) Retention policy: Confirm evidence retention N (default 10). If you want a different number, state it.
3) Secrets model: Choose where client credentials will live for demos:
   - Option A: Use GitHub Actions secrets + local `.env` on developer machines (recommended)
   - Option B: Use an external secret store (Vault/Azure Key Vault) — I will need access instructions
4) CI run approval: Run the `trinus_demo_ci.yml` workflow on push (manual dispatch available) — yes/no
5) Template decision: Should we keep demos in this repo or create a template repo per client? (choose `same-repo` or `template-repo`)

Planned automated steps once you approve (sequence)
-------------------------------------------------
1. If you approve (1), push `feature/trinus-demo` to `origin` and optionally trigger CI.
2. Add an `--env` switch and small resolver: implement config/clients/<client>.yaml reading with environment override; commit on `feature/trinus-demo`.
3. Implement FlakyGuard pytest fixture: basic retries + final screenshot/DOM snapshot on failure; commit.
4. Add Live Artifacts Streamlit panel hook that reads `artifacts/<client>/` and lists runs (scaffolded UI already); commit.
5. Run local smoke tests (Streamlit + Selenium) and report results. If OK, optionally run CI workflow.

Notes about `task_prioritizer.py` execution
------------------------------------------
- The prioritizer script failed to run due to a small bug (uses `field(Task)` incorrectly). Fix: replace `field(Task)` with `fields(Task)` from `dataclasses`.
- If you want automated, repeatable prioritization, I can patch the script, run it, and write the prioritizer output to `docs/innercouncil_priorities.txt` for future peer review.

Deliverables stored in repo now
------------------------------
- `ui_streamlit/pages/trinus_demo.py` — Streamlit demo scaffold
- `config/clients/trinus.yaml` — Trinus config defaults
- `tools/evidence_manager.py` — artifact creation & prune utils
- `tests/selenium/test_trinus_streamlit.py` — Selenium smoke test (scaffold)
- `.github/workflows/trinus_demo_ci.yml` — CI workflow (scaffold)

Proposed short next step (low-friction)
--------------------------------------
Ask: Please confirm the 3 quick items below so InnerCouncil can instruct automation to act:

1. Push approval: `yes` to push `feature/trinus-demo` to origin now.
2. Retention N: either accept `10` or provide new integer.
3. Secrets model: pick Option A (GitHub secrets + local `.env`) or Option B (external store).

If you confirm those three, the InnerCouncil will instruct automation to:
- push branch (backup),
- add an `--env` flag and config resolver, and
- run the local smoke test and report back (CI kept manual until you approve).

What InnerCouncil needs you to say (exact text)
----------------------------------------------
Please reply with a three-line approval like this (copy & paste and edit):

PUSH_FEATURE_BRANCH: yes
RETENTION_N: 10
SECRETS_MODEL: A

After that, I will execute the agreed automated steps and report results, including adding a peer-reviewable `docs/innercouncil_priorities.txt` (if you want me to fix and run the prioritizer script first, say `RUN_PRIORITIZER: yes`).

— InnerCouncil (synthetic), delivered by the automation orchestrator
