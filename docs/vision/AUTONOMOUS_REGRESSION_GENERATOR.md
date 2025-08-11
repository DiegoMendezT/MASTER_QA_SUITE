# Vision: The Surveyor Engine

**Version:** 0.1  
**Date:** 2025-08-10  
**Author:** InnerCouncil (Architect)
**Status:** Proposed

## 1. Core Vision

The Surveyor Engine is a planned, post-Alpha feature set that will transform the `MASTER_QA_SUITE` from a test execution framework into an **Autonomous Regression Generator**.

The core idea, proposed by the Release Captain, is to create a module that can be deployed in a client's environment and perform the following actions autonomously:

1.  **Analyze:** Intelligently crawl a target web application from a given root URL.
2.  **Understand:** Discover all pages, navigation flows, and interactive web elements (forms, buttons, links).
3.  **Formalize:** Treat the current, live state of the application as the implicit, approved set of requirements.
4.  **Generate:** Automatically create the corresponding artifacts needed for a full regression suite:
    *   Page Object Model classes for every discovered page.
    *   A comprehensive set of test cases to validate the application's state and functionality.

This engine will build the initial regression suite, expanding in a "fractal" pattern to ensure broad coverage with minimal human intervention.

## 2. Phased Development Plan

To manage complexity and deliver value incrementally, the Surveyor Engine will be developed in four distinct phases.

### Phase 1: The Site Mapper (v1.1)

-   **Goal:** Create a robust web crawler capable of mapping an entire web application.
-   **Inputs:** A single root URL.
-   **Outputs:** A structured data file (e.g., JSON, YAML) representing the full site map, including all unique pages and the links between them.
-   **Focus:** Pure discovery and mapping.

### Phase 2: The DOM Analyzer (v1.2)

-   **Goal:** Enhance the Site Mapper to analyze the content of each discovered page.
-   **Inputs:** The site map from Phase 1.
-   **Outputs:** An enriched data file where each page is annotated with a list of all "Web Elements of Interest" (WEIs) and their optimal locators (ID, name, CSS selector, XPath). This file becomes the auto-generated requirements baseline.
-   **Focus:** Element identification and locator strategy.

### Phase 3: The Page Object Generator (v1.3)

-   **Goal:** Convert the structured data from the DOM Analyzer into functional code.
-   **Inputs:** The enriched data file from Phase 2.
-   **Outputs:** A complete set of boilerplate Page Object Model classes (`.py` files) placed in a `pages/generated/` directory. Each class will correspond to a page, and each attribute will correspond to a WEI.
-   **Focus:** Code generation and project structure integration.

### Phase 4: The Test Scaffolder (The "Fractal" Engine) (v1.4)

-   **Goal:** Use the generated Page Objects to build a baseline suite of executable tests.
-   **Inputs:** The generated Page Object classes and the site map.
-   **Outputs:** A suite of `test_*.py` files containing a variety of foundational tests:
    -   **Smoke Tests:** Verify each page loads and key elements are present.
    -   **Navigation Tests:** Assert that all links correctly navigate to their intended destination.
    -   **Interaction Stubs:** Create placeholder test functions for more complex user flows (e.g., filling and submitting every form).
-   **Focus:** Test logic, assertions, and creating a comprehensive, ready-to-run regression suite.

## 3. Strategic Importance

The Surveyor Engine is the key to the framework's scalability and rapid deployment for new clients. It fulfills the promise of not just providing a tool, but providing an immediate, tangible result with minimal setup cost.
