"""
Test: Navigation and Title Assertion
Selenium/API Features: [driver.get, driver.title, assert]
AUT: The Internet
Markers: @ui
Purpose: Verifies the basic ability to navigate to a URL and assert the page title. This is the foundational step for all UI tests.
"""
import pytest
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def save_ui_screenshot(driver, name):
    screenshot_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'artifacts', 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path


@pytest.mark.ui
def test_01_navigate_and_assert_title(driver, config):
    """
    Tests navigation to The Internet homepage and asserts the title.
    """
    # Arrange: Get the URL from the config file
    the_internet_url = config['urls']['the_internet']

    # Act: Navigate to the URL
    driver.get(the_internet_url)
    save_ui_screenshot(driver, "test_01_navigate_and_assert_title_navigated")

    # Assert: Check that the page title is correct
    expected_title = "The Internet"

    # Use WebDriverWait to wait for the title to be correct
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(expected_title))
    except:
        pass # Allow the assertion to handle the failure message

    actual_title = driver.title
    save_ui_screenshot(driver, "test_01_navigate_and_assert_title_final")

    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in actual title '{actual_title}'"
