"""
Custom exceptions for the test framework.
"""

class ElementNotFoundException(Exception):
    """Raised when an element cannot be found on the page."""

class ElementInteractionException(Exception):
    """Raised when an interaction with an element fails."""
