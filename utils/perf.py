
"""
Project: MASTER_QA_SUITE
Module: utils/perf.py
Purpose: Performance utilities for browser/page load metrics and timing analysis.
Voices: Architect, Engineer, QA, Gatekeeper, Release Captain, Product Owner, Shadow QA, Copilot
Traceability: decision_log.md:2025-08-10 entry; roadmap.md:Performance; requirements:perf-001
Notes: Freeze-safe; no behavior change. [Kintsugi]
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
    import time
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            timing = driver.execute_script("return window.performance.timing.toJSON();")
            if timing and timing.get('loadEventEnd', 0) > 0:
                return timing
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Could not retrieve navigation timing: {e}")
            break
    logging.warning(f"Navigation timing data invalid or incomplete: {timing if 'timing' in locals() else '{}'}")
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
