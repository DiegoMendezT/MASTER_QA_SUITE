# Master Rules of Governance

**Version:** 1.0  
**Date:** 2025-08-10 13:45 UTC  
**Author:** [Architect as Copilot]

## Preamble: The Akashic Records

This document is the constitution of the `MASTER_QA_SUITE` project. It contains the foundational rules that govern our development, decision-making, and evolution. The `/docs` directory, in its entirety, constitutes the project's **Akashic Records**—the immutable, single source of truth for our history, wisdom, and intent.

---

## The 18 Foundational Rules

1.  **The Kintsugi Philosophy:** We improve the project by adding "gold seams"—enhancing documentation, governance, and vision—especially during code freezes.
2.  **The Accountability Field:** Every action and artifact is traceable and accountable to a voice and an actor.
3.  **Strict Client Separation:** This repository is the master template. It will NEVER contain client-specific code.
4.  **Total Inheritance:** Client clones receive the ENTIRE system: code, tests, and the full governance/memory framework.
5.  **Evidence as ROM:** All test outputs are Read-Only Memory—immutable, timestamped, and containing origin metadata.
6.  **The Surveyor Engine Vision:** The post-Alpha goal is to build an Autonomous Regression Generator, as detailed in the vision document.
7.  **The `SaveToMemory()` Directive:** The AI must perform a comprehensive update of the Akashic Records when this command is given.
8.  **The "Diego Alejandro" Persona:** The designated operator for all client deployments is "Diego Alejandro." The deployment process must be designed for him.
9.  **The Superclass Mandate:** This repo is the "Superclass," the client's is the "Subclass," and the operator is fully empowered on Deployment Day.
10. **Template-Based Extensibility:** The framework will provide templates for docs and tests to ensure client-side extensibility.
11. **The Rule of Rules:** New rules are saved to this master file. The AI must check for conflicts before adding a new rule.
12. **The Attribution Mandate:** Decisions are attributed to both a symbolic `InnerCouncil` voice and the real-world actor who channeled it (e.g., `[Architect as Release Captain]`).
13. **The InnerCouncil Exemption:** The `InnerCouncil`'s own code (`tools/task_prioritizer.py`) is exempt from a hard code freeze to allow it to evolve.
14. **The Synthesis Protocol:** The AI must operate on a three-stage decision loop: 1) Form its own analysis, 2) Simulate the `InnerCouncil`'s response, 3) Present a final, synthesized decision.
15. **The Intentionality Mandate:** All logged decisions must include the core *intent* of the voice that made them.
16. **The Release State Policy:** For a specific release tag, all executable code (including the `InnerCouncil`) is frozen. The Akashic Records remain live.
17. **The Continuous Evolution Protocol:** The `InnerCouncil`'s code is a "Live" file that grows with each decision. Before each evolution, a timestamped snapshot is saved to `tools/history/` to ensure a rollback path.
18. **The Next Steps Mandate:** After every action, audit, or decision, the system (AI or human) must print or record the next steps to be taken. This ensures continuous guidance, transparency, and traceability for all contributors.

19. **The Prompt-to-Record Rule:** Every prompt, decision, or action must result in an update to the Akashic Records (decision log, checkpoints, or governance docs), ensuring traceability, compliance, and a living project memory. No prompt is ephemeral; all are recorded. Every next steps report must include the names of the files that were updated for memory and voice logic.
