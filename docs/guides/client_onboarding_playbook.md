# Client Onboarding Playbook

**Version:** 1.0  
**Date:** 2025-08-10  
**Author:** InnerCouncil (Architect)

## 1. Philosophy

This document outlines the standard operating procedure for deploying the `MASTER_QA_SUITE` for a new client engagement. The core principle is **separation and extension**. The master repository remains a pristine, generic template, while each client receives a dedicated, cloned instance to house their specific tests, configurations, and documentation.

This approach prevents client-specific logic from leaking into the core framework and allows for independent development cycles.

## 2. Onboarding Process

The process begins *after* a stable, shippable version of the `MASTER_QA_SUITE` has been tagged and released.

### Step 1: Project Scaffolding

1.  **Clone the Master Repository:** Create a new, private repository for the client (e.g., `client-accenture-qa`). Clone the latest stable release of `MASTER_QA_SUITE` into this new repository.
    ```bash
    git clone --depth 1 --branch v1.0.1 <URL_TO_MASTER_QA_SUITE> ./client-accenture-qa
    ```
2.  **Isolate History:** Remove the original `.git` directory and re-initialize a new git history for the client's project. This ensures the client's repository starts with a clean slate.
    ```bash
    cd ./client-accenture-qa
    rm -rf .git
    git init
    git add .
    git commit -m "feat: initial commit from MASTER_QA_SUITE v1.0.1"
    ```

### Step 2: Environment Setup (In a New VM)

1.  **Provision a Clean VM:** Set up a new, clean Virtual Machine that mirrors a typical developer environment.
2.  **"Unpack" the Project:** Transfer the cloned client project into the VM.
3.  **Run Verification Scripts:** Execute the framework's setup and verification scripts (`verify_setup.py`) to ensure all dependencies are correctly installed and the environment is sound. This step is critical for validating the "unpacking" process itself.

### Step 3: Configuration

1.  **Configure Target URL:** In the client's repository, modify the relevant configuration files (e.g., `config/settings.yml`) to point to the client's target application URL (e.g., `https://www.accenture.com`).
2.  **Set Up Credentials:** Add any necessary test account credentials to the secure credential management system. **DO NOT** commit credentials to the repository.

### Step 4: Initial Test Development

1.  **Create First Test:** Develop the first end-to-end user journey test for the client (e.g., `tests/client/test_01_main_user_flow.py`). This test serves as a proof-of-concept and validates the entire setup.
2.  **Run and Verify:** Execute the test and confirm that it runs successfully against the client's live or staging environment.

### Step 5: Handover

1.  **Document Client-Specifics:** Create a `README.md` in the client's repository that details any specific setup steps, test data, or operational notes.
2.  **Grant Access:** Provide the client team with access to their new, dedicated QA repository.

### Step 6: Client Handover & Total Inheritance

1.  **Document Client-Specifics:** Create a `README.md` in the client's repository that details any specific setup steps, test data, or operational notes.
2.  **Grant Access:** Provide the client team with access to their new, dedicated QA repository.
3.  **Confirm Total Inheritance:** The handover process includes confirming that the client's cloned repository contains the complete feature set of the master `MASTER_QA_SUITE`, including all self-testing, documentation, governance, and memory systems. The client receives the full, accountable platform.

This playbook ensures a repeatable, secure, and isolated process for every new client engagement.
