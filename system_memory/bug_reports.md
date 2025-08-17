# Bug Reports Log

## 2025-08-10

---
**BUG-20250810-001**
**Title:** Parallel execution set to Off but not running serially
- **Evidence:** Screenshot showing multiple [gwX] workers in output, parallel test execution, even when UI set to serial.
- **URL:** http://localhost:8503
- **Status:** Closed
- **SDLC Status:** Fixed
- **Dependencies:** Streamlit UI, pytest command builder
- **Traceability:** UI: Parallel execution selector, Test: all (serial/parallel)
- **Reported by:** Diego
- **Closed on:** 2025-08-10

---
**BUG-20250810-002**
**Title:** Download HTML report refreshes runner results
- **Evidence:** User report, UI behavior: clicking Download HTML Report causes Streamlit to rerun and refresh results.
- **URL:** http://localhost:8503
- **Status:** Closed
- **SDLC Status:** Fixed
- **Dependencies:** Streamlit UI, download_button
- **Traceability:** UI: Results & Artifacts, Test: manual user action
- **Reported by:** Diego
- **Closed on:** 2025-08-10

---

*This file is auto-generated for bug tracking. Attachments and further evidence can be added as needed. Closed bugs are retained for traceability.*
