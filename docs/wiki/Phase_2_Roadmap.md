# Phase 2 Roadmap — MASTER_QA_SUITE

**Status:** Planned • **Targets:** Developer Delight, Cross-Device Coverage, Course Depth  
**Why now?** v1.0.0 is stable. Phase 2 turns it from “professional” into “signature”.

## Themes
- **DX & Observability:** FlakyGuard, richer artifacts, faster root cause.
- **Config & Data:** One suite, many envs; deterministic data.
- **Coverage & Visuals:** Mobile emulation matrix + Applitools baseline mgmt.
- **Full-stack Truth:** UI↔API parity and contract tests that fail fast.
- **Course-First Docs:** Tech Heads get deep dives; leaders get outcomes.

## Acceptance Gates (Definition of Done)
- Each task ships with:
  - CLI flag / config knob
  - CI job or matrix dimension
  - Docs (README/Wiki) + demo script
  - At least one example test
  - Allure labels where applicable

## Deliverables (Link to YAML)
See `config/roadmap_phase2.yml` for machine-readable epics, tasks, and scoring.

## Demo Script (10 mins)
1. `--env=stage` switch + retry demo (forced flaky element).
2. Failure artifact tour: screenshots, DOM, trace, Allure.
3. Mobile matrix run (Pixel & iPhone) + Applitools diff review.
4. UI↔API parity check catching a seeded mismatch.
5. Docs toggle: Tech Head vs Manager mode preview.

## Risks & Mitigations
- **Matrix sprawl:** keep a slim default; extend in nightly.
- **Flaky retries hide bugs:** limit retries, surface root cause artifacts.
- **Baseline churn:** tag per-env/device; reviewer checklist in README.

## Metrics We’ll Watch
- MTTR for red builds (minutes)
- % runs with artifacts attached
- Mobile/device coverage
- Contract drift alerts per month
