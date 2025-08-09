"""
Test: UI Navigation Timing Budget
Selenium/API Features: [window.performance.timing, Custom perf utils]
AUT: The Internet
Markers: @perf @ui
Purpose: Verifies that the page load time of a simple page is within an
         acceptable performance budget.
"""
import os

import pytest

from utils.perf import calc_load_ms, get_nav_timing

# --- Test Configuration ---
# Performance budget in milliseconds for page load.
# Can be overridden by an environment variable.
UI_BUDGET_MS = int(os.environ.get("UI_BUDGET_MS", 3000))

@pytest.mark.perf
@pytest.mark.ui
def test_navigation_timing_budget(driver, config):
    """
    Tests that The Internet homepage loads within the defined time budget.
    """
    # Arrange: Get the URL from the config file
    the_internet_url = config['urls']['the_internet']
    
    # Act: Navigate to the URL and get performance timing
    driver.get(the_internet_url)
    timing = get_nav_timing(driver)
    
    # Calculate the total load time
    load_time_ms = calc_load_ms(timing)

    # Assert
    assert timing, "Could not retrieve performance timing data from the browser."
    assert load_time_ms != -1, "Invalid timing data received."
    
    print(f"Page load time: {load_time_ms}ms (Budget: {UI_BUDGET_MS}ms)")
    
    assert load_time_ms <= UI_BUDGET_MS, \
        f"Page load time ({load_time_ms}ms) exceeded budget of {UI_BUDGET_MS}ms."
