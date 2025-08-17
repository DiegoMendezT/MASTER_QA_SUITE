
"""
Project: MASTER_QA_SUITE
Module: utils/exceptions.py
Purpose: Custom exceptions for robust error handling in test framework.
Voices: Architect, Engineer, QA, Gatekeeper, Release Captain, Product Owner, Shadow QA, Copilot
Traceability: decision_log.md:2025-08-10 entry; roadmap.md:ErrorHandling; requirements:err-001
Notes: Freeze-safe; no behavior change. [Kintsugi]
"""

class ElementNotFoundException(Exception):
    """Raised when an element cannot be found on the page."""

class ElementInteractionException(Exception):
    """Raised when an interaction with an element fails."""

"""
Project: MASTER_QA_SUITE
Module: utils/exceptions.py
Purpose: Custom exceptions for robust error handling in test framework.
Voices: Architect, Engineer, QA, Gatekeeper, Release Captain, Product Owner, Shadow QA, Copilot
Traceability: decision_log.md:2025-08-10 entry; roadmap.md:ErrorHandling; requirements:err-001
Notes: Freeze-safe; no behavior change. [Kintsugi]
"""
