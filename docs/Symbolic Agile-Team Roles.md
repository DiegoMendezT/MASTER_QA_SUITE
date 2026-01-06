# InnerCouncil — Roles & Responsibilities (Trinus Demo)

This file extracts the "Council composition" from `docs/INNERCOUNCIL_TRINUS_DELIBERATION.md` and presents a compact agile-style roles table for quick reference.

| Role | Primary Focus | Decisions / Authority | Acceptance Criteria (for MVP work) |
|------|---------------|-----------------------|------------------------------------|
| QA Director (QA) | Stability, reproducibility, reliability | Accept/reject FlakyGuard, Live Artifacts; sign off on release demo quality | Demos run reliably (<= 1 flake / 10 runs), artifacts are inspectable and shareable |
| Automation Engineer (AE) | Implementability, CI, parallel runs | Choose implementation approach for Env switcher, FlakyGuard, test fixtures | Tests run in CI and locally; parallel workers work (sample smoke pass) |
| Product Owner (PO) | ROI, demo polish, business value | Prioritize Live Artifacts and Visual Baseline; accept demo for stakeholder review | Demo meets acceptance demo checklist (screenshots, run metadata, demo flow) |
| ML Researcher (ML) | Future learning & capabilities | Advocate for features that enable ML reuse (data factory, contract tests) | Data fixtures available; ML metrics captured (if applicable) |
| Compliance / Security (Sec) | Secrets & policy, risk control | Block unsafe secret handling; approve secrets model (A or B) | No secrets in repo; secrets flow follows the approved model |

Notes
- These roles are "synthetic" voices recorded by the InnerCouncil deliberation. Use this table as a short reference for who owns what decisions during the Trinus MVP.
- For any automated action that pushes to remote or modifies CI, the InnerCouncil requires explicit human confirmation (see `docs/INNERCOUNCIL_TRINUS_DELIBERATION.md`).

Generated from `docs/INNERCOUNCIL_TRINUS_DELIBERATION.md` on 2025-12-16.
