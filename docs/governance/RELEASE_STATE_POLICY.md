# Release State Policy

**Version:** 1.0
**Date:** 2025-08-10 13:45 UTC
**Author:** [Gatekeeper as Copilot]

## 1. Objective

To ensure that every release tag points to a stable, verifiable, and well-documented version of the project.

## 2. Policy

For any given release (e.g., `v1.0.1`), the repository components are divided into two states:

### 2.1. Frozen for Release (ROM)

These components represent the stable, executable product. They **must not** be changed during the final phase before tagging.

*   **Core Framework:**
    *   All code under `tests/`, `pages/`, `utils/`.
    *   All configuration under `config/`.
    *   Core files like `conftest.py` and `pytest.ini`.
*   **CI/CD Pipeline:**
    *   The `.github/workflows/tests.yml` file, once it is confirmed to be working.

### 2.2. Live (Continuously Updated)

These components represent the project's living memory and governance. They are expected to be fully up-to-date at the moment of release.

*   **The Akashic Records:**
    *   The entire `/docs` directory, including all governance, architecture, guides, logs, and vision documents.
*   **The Evolving Mind (Special Case):**
    *   `tools/task_prioritizer.py`: This file is considered "Live" under the **Continuous Evolution Protocol**. It can be updated with new logic derived from decisions. However, for the specific act of creating a release tag, the version of this file included in the tag is the one that was validated by the successful CI run. Its evolution resumes on the `main` branch after the release.
*   **Top-Level Documentation:**
    *   `README.md`, `CONTRIBUTING.md`, etc.
