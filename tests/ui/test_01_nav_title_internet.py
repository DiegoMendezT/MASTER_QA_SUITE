"""
Test: Navigation and Title Assertion
Selenium/API Features: [driver.get, driver.title, assert]
AUT: The Internet
Markers: @ui
Purpose: Verifies the basic ability to navigate to a URL and assert the page title. This is the foundational step for all UI tests.
"""
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.ui
def test_01_navigate_and_assert_title(driver):
    """
    Tests navigation to The Internet homepage and asserts the title.
    """
    # Act: Navigate to the URL
    driver.get("https://the-internet.herokuapp.com/")
    
    # Assert: Check that the page title is correct
    expected_title = "The Internet"
    
    # Use WebDriverWait to wait for the title to be correct
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(expected_title))
    except:
        pass # Allow the assertion to handle the failure message
        
    actual_title = driver.title
    
    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in actual title '{actual_title}'"
