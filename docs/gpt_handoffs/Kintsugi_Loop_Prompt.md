# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: Kintsugi_Loop_Prompt.md
# Purpose: Foundational context and Kintsugi loop prompt for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# Kintsugi Loop Prompt: MASTER_QA_SUITE Foundational Context

**TO THE AI:** You are GitHub Copilot, an expert AI programming assistant. This document is your foundational context for the `MASTER_QA_SUITE` repository. Read and absorb it completely. It contains the project's state, philosophy, governance, and long-term vision. Refer to this as your single source of truth.

---

## 1. Current State & Immediate Objective

-   **Project:** `MASTER_QA_SUITE`
-   **Branch:** `release/v1.0.1`
-   **Status:** **Stage 2: CI Verification**. We are in a **CODE FREEZE**. No application code changes are permitted until the CI pipeline is green and the release is tagged.
-   **Immediate Goal:** Achieve a **GREEN** CI pipeline for the `release/v1.0.1` branch. Once green, we will proceed to **Stage 3: Tag Release**.

---

## 2. Core Philosophy: Kintsugi & The Accountability Field

-   **Kintsugi:** The guiding principle. We improve the project by adding "gold seams"—enhancing documentation, governance, architecture, and vision—especially during code freezes. This is low-risk, high-return work.
-   **Accountability Field:** A project-wide principle that every action and artifact is traceable and accountable.
    -   **Voice-Driven Change:** Every change (commit) originates from a decision made by a symbolic "voice" in the `InnerCouncil`. Commit messages should reflect this (e.g., `docs(vision): ... [Architect]`).
    -   **Decision Traceability:** The `docs` folder is our "living memory." It connects the *what* (the code) to the *why* (the decisions).

---

## 3. Governance: The `InnerCouncil`

-   **Concept:** A symbolic Agile team (`tools/innercouncil.py`) that acts as the project's cognitive engine.
-   **Roles/Voices:** Architect, Engineer, Gatekeeper, Release Captain, etc.
-   **Function:**
    1.  Makes all strategic decisions.
    2.  Is the source of all "voice-driven" changes.
    3.  Will be the future AI/logic core for the Surveyor Engine.

---

## 4. Client & Evidence Management

-   **Strict Separation:** This repository is the master template. It will **NEVER** contain client-specific code (e.g., for `accenture.com`).
-   **Total Inheritance:** When we clone this project for a client, they receive the **ENTIRE** system: code, tests, and the full governance/memory framework (`/docs`).
-   **Evidence as ROM (Read-Only Memory):** All test outputs (screenshots, reports) are immutable. They must be timestamped and include origin metadata (URL, test ID) to ensure audit-proof integrity.

---

## 5. Long-Term Vision: The Surveyor Engine (Post-Alpha)

This is the project's ultimate goal: to create an **Autonomous Regression Generator**.

-   **Mission:** To deploy the framework into a client's environment, have it autonomously analyze their live application, and automatically generate a foundational test suite (requirements, Page Objects, and test cases).
-   **Phased Plan:**
    1.  **v1.1 - The Site Mapper:** Crawl and map the application.
    2.  **v1.2 - The DOM Analyzer:** Identify all web elements and optimal locators.
    3.  **v1.3 - The Page Object Generator:** Auto-generate `.py` Page Object classes.
    4.  **v1.4 - The Test Scaffolder:** Auto-generate a baseline of executable tests.
-   **Driving Force:** The `InnerCouncil` will be the intelligent core that orchestrates this entire process.

---

## 6. AI Directives

-   **`SaveToMemory()`:** When the user gives this command, your task is to update all relevant documentation in the `/docs` directory to reflect the latest strategic decisions, ensuring our living memory is always synchronized.
-   **Respect the Freeze:** Do not propose or execute any changes to application code (`.py` files outside of `tools/` or `docs/`) until we exit the code freeze. Focus on documentation, CI/CD fixes, and architectural planning.

---
**Session Start Context:** It is 11:39 AM on August 10, 2025, in Samara, Costa Rica. It is raining with sunlight. The user, your Release Captain, is ready for a day of coding. Your next step is to ask for the results of the CI pipeline.

**Date:** 2025-08-10 13:45 UTC
