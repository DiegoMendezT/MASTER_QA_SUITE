"""
Test: Navigation and Title Assertion
Selenium/API Features: [driver.get, driver.title, assert]
AUT: The Internet
Markers: @ui
Purpose: Verifies the basic ability to navigate to a URL and assert the page title. This is the foundational step for all UI tests.
"""
import pytest

@pytest.mark.ui
def test_01_navigate_and_assert_title(driver, config):
    """
    Tests navigation to The Internet homepage and asserts the title.
    """
    # Arrange: Get the URL from the config file
    the_internet_url = config['urls']['the_internet']
    
    # Act: Navigate to the URL
    driver.get(the_internet_url)
    
    # Assert: Check that the page title is correct
    expected_title = "The Internet"
    actual_title = driver.title
    
    assert expected_title in actual_title, f"Expected title '{expected_title}' not found in actual title '{actual_title}'"
