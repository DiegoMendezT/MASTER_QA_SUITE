# Packaging and Deployment Guide

**Version:** 1.0
**Date:** 2025-08-10 13:45 UTC
**Author:** [Architect as Copilot]

## 1. The Superclass Mandate

This `MASTER_QA_SUITE` repository is the **"Superclass"**—the master blueprint. A client's instance is a **"Subclass"** that inherits all of its power. This guide outlines the process for creating and deploying a new client instance.

## 2. Target Operator Persona: "Diego Alejandro"

This entire process is designed for a designated operator, "Diego Alejandro." The operator is assumed to be working on a clean laptop, with access to GitHub and a target client environment (e.g., a fresh VM). On "Deployment Day," the operator is granted the full, untethered power of the superclass to make the client's instance a success.

## 3. Deployment Workflow

### Step 1: Create the Client Package
1.  **Clone the Master Repo:** From the `main` branch of `MASTER_QA_SUITE`, clone the repository to a new local directory.
    ```bash
    git clone https://github.com/DiegoMendezT/MASTER_QA_SUITE.git ./client-package
    ```
2.  **Run the Clean-Up Script:** Execute the packaging script to prepare the clone for distribution. This script will:
    *   Remove the `.git` directory.
    *   Delete development-specific history and logs (e.g., `docs/gpt_handoffs/`, `docs/checkpoints/`, `tools/history/`).
    *   Scrub any development-specific entries from `docs/decision_log.md`.
    *   **(Future):** This script will be located at `scripts/package_project.py`.
3.  **Zip the Package:** Create a zip archive of the cleaned directory (e.g., `MASTER_QA_SUITE_CLIENT_v1.0.1.zip`).

### Step 2: Onboard the Client
This process is detailed in the `docs/guides/client_onboarding_playbook.md`. It involves setting up the client's own private repository, transferring the package to their environment, and running the initial setup.

### Step 3: Activate Templates
Once unpacked in the client's environment, the operator will:
1.  Copy the contents of `docs/templates/` into the root `docs/` directory.
2.  Copy the contents of `tests/templates/` into the `tests/` directory.
3.  This provides the client with a clean, best-practice starting point for their own documentation and test suite.
