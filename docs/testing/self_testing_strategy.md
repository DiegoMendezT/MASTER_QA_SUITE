# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: self_testing_strategy.md
# Purpose: Describes the self-testing and quality strategy for the MASTER_QA_SUITE project.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 13:45 UTC
#
# This file is part of the Akashic Records. All changes must be attributed and timestamped.

# Self-Testing and Quality Strategy

**Version:** 1.0
**Date:** 2025-08-10 13:45 UTC
**Author:** [Gatekeeper as Copilot]

## 1. Philosophy

The `MASTER_QA_SUITE` must be as reliable as the applications it is designed to test. To achieve this, the framework practices what it preaches: it has its own internal, automated test suite.

This self-testing strategy ensures that the core framework logic, utilities, and decision-making engines are robust, reliable, and regression-proof.

## 2. Scope of Self-Testing

The self-testing suite, located under `/tests/internal/`, covers the following key areas:

### 2.1. Core Utilities (`/utils`)
-   Unit tests for all helper functions, guards, and clients.
-   Ensures that foundational components like `flaky_guard` and `selenium_guard` behave as expected.

### 2.2. Page Object Base (`/pages/base_page.py`)
-   Tests for the `BasePage` class to validate its core methods (`find_element`, `click`, `fill_text`, etc.) work correctly across both Selenium and Playwright engines.

### 2.3. The InnerCouncil (`/tools/task_prioritizer.py`)
-   This is the most critical component of the self-testing suite.
-   **Unit Tests:** Validate the scoring algorithms (`wsjf`, `rice`, `linear`) with known inputs and expected outputs.
-   **Integration Tests:** Test the command-line interface, including argument parsing and file I/O for `backlog.yml`.
-   **Evolutionary Tests:** As the `InnerCouncil` evolves, its test suite will grow to cover new voices and decision logic, ensuring that adding new capabilities does not break existing ones.

## 3. Execution in CI/CD

-   The self-testing suite is a dedicated job in the `.github/workflows/tests.yml` pipeline.
-   It is marked with `@pytest.mark.internal`.
-   The pipeline is configured to run these tests first. If the framework itself is broken, there is no point in running the UI tests for external applications. This is a "fail-fast" strategy.

## 4. Client Inheritance

-   The self-testing suite is included in the package deployed to clients.
-   This provides them with a powerful diagnostic tool to verify that the framework is functioning correctly in their own environment.
