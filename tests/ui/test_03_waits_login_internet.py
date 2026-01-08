"""
Test: Explicit Waits
Selenium/API Features: [WebDriverWait, EC.visibility_of_element_located]
AUT: The Internet
Markers: @ui
Purpose: To demonstrate the use of explicit waits (WebDriverWait) to handle dynamic elements that may not be immediately present on the page. This is a critical technique for avoiding flaky tests.
"""
import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def save_ui_screenshot(driver, name):
    screenshot_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'artifacts', 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path


@pytest.mark.ui
def test_03_explicit_waits_for_dynamic_element(driver, config):
    """
    Tests waiting for a dynamically loaded element to appear.
    """
    # Arrange: Navigate to the "Dynamic Loading" example page
    driver.get(config['urls']['the_internet'] + "/dynamic_loading/2")
    save_ui_screenshot(driver, "test_03_explicit_waits_navigated")

    # Act: Click the "Start" button to trigger the loading of a new element
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    start_button.click()
    save_ui_screenshot(driver, "test_03_explicit_waits_after_start")

    # Assert: Use WebDriverWait to wait for the "Hello World!" text to be visible
    # This is the key part of the test. We wait up to 10 seconds for the element.
    wait = WebDriverWait(driver, 10)
    finish_element = wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    save_ui_screenshot(driver, "test_03_explicit_waits_after_hello_world")

    # Verify the text of the element that appeared
    assert "Hello World!" in finish_element.text, "The expected 'Hello World!' text was not found."
