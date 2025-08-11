# MASTER_QA_SUITE
# Project: MASTER_QA_SUITE
# File: flaky_guard.py
# Purpose: Retry system for transient errors, used for robust automation and test reliability.
# Maintainer: DiegoMendezT / InnerCouncil
# Last updated: 2025-08-10 14:00 UTC
#
# Agile Voice Attribution (Full Team):
# - Product Owner, Scrum Master, Development Team, Stakeholders, Subject Matter Experts
# - QA Voice: [Diego Alejandro], Shadow QA: [Diego's Shadow]
# - Teacher as Copilot, Gatekeeper as Copilot, Release Captain
#
# All major changes must be attributed in docs/decision_log.md.

# utils/flaky_guard.py
"""
A robust decorator-based retry system to handle transient errors,
making functions and classes more resilient to intermittent failures.

This module provides:
- A `retry_on` function decorator for fine-grained retry logic.
- A `FlakyGuard` class decorator that automatically applies retry logic
  to all public methods of a class, perfect for Page Object Models.
"""
from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Callable, Iterable, Tuple, Type

# --- Configuration ---
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF = 0.35  # seconds; jitter-free for readable logs
LOG = logging.getLogger(__name__)

# --- Exceptions to Retry On ---
# A default set of common, transient Selenium exceptions.
# These are often resolved by a simple retry.
DEFAULT_RETRY_EXCEPTIONS = (
    "StaleElementReferenceException",
    "ElementClickInterceptedException",
    "ElementNotInteractableException",
    "TimeoutException",
    "NoSuchElementException",
    "WebDriverException"  # General catch-all for driver issues
)

def _get_selenium_exceptions(exception_names: Iterable[str]) -> Tuple[Type[BaseException], ...]:
    """
    Dynamically imports Selenium exceptions to avoid a hard dependency if
    this utility is used in a non-Selenium context.
    """
    exceptions = []
    try:
        # Lazy import inside the function
        from selenium.common.exceptions import (
            ElementClickInterceptedException, ElementNotInteractableException,
            NoSuchElementException, StaleElementReferenceException,
            TimeoutException, WebDriverException)
        exception_map = {
            "StaleElementReferenceException": StaleElementReferenceException,
            "ElementClickInterceptedException": ElementClickInterceptedException,
            "ElementNotInteractableException": ElementNotInteractableException,
            "TimeoutException": TimeoutException,
            "NoSuchElementException": NoSuchElementException,
            "WebDriverException": WebDriverException,
        }
        for name in exception_names:
            if name in exception_map:
                exceptions.append(exception_map[name])
    except ImportError:
        LOG.warning("Selenium library not found. FlakyGuard will only handle generic Exceptions.")
    
    # Always include the base Exception as a fallback
    if not exceptions:
        return (Exception,)
    return tuple(exceptions)

def retry_on(
    exceptions: Iterable[Type[BaseException]],
    tries: int = DEFAULT_RETRIES,
    backoff: float = DEFAULT_BACKOFF
) -> Callable:
    """
    A function decorator to automatically retry on a given set of exceptions.

    Args:
        exceptions (Iterable[Type[BaseException]]): A tuple of exception types to catch.
        tries (int): The maximum number of attempts.
        backoff (float): The base delay between retries in seconds.
    """
    def deco(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_err: BaseException | None = None
            for attempt in range(1, tries + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    LOG.warning(
                        f"Attempt {attempt}/{tries} failed for '{fn.__name__}' "
                        f"due to {e.__class__.__name__}. Retrying..."
                    )
                    last_err = e
                    if attempt >= tries:
                        LOG.error(f"All {tries} retries failed for '{fn.__name__}'. Raising final exception.")
                        raise
                    # Linear backoff keeps test execution time predictable
                    time.sleep(backoff * attempt)
            # This line is theoretically unreachable but here for type safety
            raise last_err  # type: ignore
        return wrapper
    return deco

def FlakyGuard(
    retries: int = DEFAULT_RETRIES,
    backoff: float = DEFAULT_BACKOFF,
    exceptions_to_retry: Iterable[str] = DEFAULT_RETRY_EXCEPTIONS
):
    """
    A class decorator that applies retry logic to all public methods of a class.

    This is ideal for Page Object Models, where any interaction with a web
    element could potentially be flaky.

    Args:
        retries (int): Max number of attempts for each method call.
        backoff (float): Base delay between retries.
        exceptions_to_retry (Iterable[str]): String names of exceptions to handle.
    """
    selenium_exceptions = _get_selenium_exceptions(exceptions_to_retry)

    def decorator(cls):
        # Iterate over class attributes
        for attr_name, attr_value in cls.__dict__.items():
            # Apply only to public methods (callable and not starting with '_')
            if callable(attr_value) and not attr_name.startswith('_'):
                # Wrap the method with the retry decorator
                decorated_method = retry_on(
                    exceptions=selenium_exceptions,
                    tries=retries,
                    backoff=backoff
                )(attr_value)
                setattr(cls, attr_name, decorated_method)
        return cls
    return decorator
