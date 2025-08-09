"""
Performance Utilities for MASTER QA SUITE

This module provides helper functions for performance testing, such as
retrieving navigation timing metrics from the browser.
"""
import logging

def get_nav_timing(driver) -> dict:
    """
    Retrieves the window.performance.timing object from the browser.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        A dictionary containing the performance timing attributes.
        Returns an empty dictionary if the timing object is not available.
    """
    try:
        return driver.execute_script("return window.performance.timing.toJSON();")
    except Exception as e:
        logging.error(f"Could not retrieve navigation timing: {e}")
        return {}

def calc_load_ms(timing: dict) -> int:
    """
    Calculates the total page load time from a performance timing object.

    Args:
        timing: A dictionary of performance timing attributes.

    Returns:
        The total page load time in milliseconds.
        Returns -1 if the timing data is invalid.
    """
    if not timing or 'loadEventEnd' not in timing or 'navigationStart' not in timing:
        return -1
    
    load_time = timing['loadEventEnd'] - timing['navigationStart']
    return load_time if load_time >= 0 else -1
