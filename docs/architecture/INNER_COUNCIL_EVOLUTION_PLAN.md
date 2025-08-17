# InnerCouncil Evolution Plan

**Version:** 1.0
**Date:** 2025-08-10 13:45 UTC
**Author:** [Architect as Copilot]

## 1. Vision

The `InnerCouncil`, currently represented by `tools/task_prioritizer.py`, must evolve from a simple command-line script into a fully autonomous, AI-driven decision engine. This is the core of the project's long-term vision for self-governance and autonomous operation.

## 2. The Continuous Evolution Protocol

The `InnerCouncil`'s code is designated a "Live" file. It is expected to grow and mature with every major decision the project makes. To ensure stability, this evolution is governed by two principles:

1.  **Historical Snapshots:** Before any change is applied to the live `task_prioritizer.py`, a timestamped copy of the current version will be saved to `tools/history/`. This creates a complete, traceable history of its evolution and provides a safe rollback path.
2.  **Dedicated Test Suite:** A post-release goal is to develop a dedicated test suite (`tests/tools/test_task_prioritizer.py`) to validate the Council's logic. This will run with every change, preventing regressions in its decision-making capabilities.

## 3. Phased Development Plan

The evolution will occur in four distinct phases:

*   **Phase 1 (Current - v1.0.1): A Command-Line Shim.**
    *   A single script that provides basic task prioritization. The "voices" are conceptual and simulated by the AI agent.

*   **Phase 2 (Post-Release): Class-Based Refactor.**
    *   Refactor `task_prioritizer.py` into a primary `InnerCouncil` class.
    *   Each "Voice" (Architect, Engineer, etc.) will be implemented as a method or a dedicated helper class within this structure.

*   **Phase 3 (Advanced): Plugin-Based Architecture.**
    *   Evolve into a plugin-based system. The core `InnerCouncil` engine will load "Voice" plugins from a dedicated directory (e.g., `tools/voices/`).
    *   This allows each voice's logic to grow independently in its own file, making the system highly modular and extensible.

*   **Phase 4 (Autonomous): The Decision Engine Service.**
    *   The `InnerCouncil` becomes a full decision-making service that the primary AI agent (Copilot) can query via a defined API.
    *   At this stage, the AI-Clocked Governance model becomes a reality. The AI will be truly governed by the project's own internal, evolving logic.
