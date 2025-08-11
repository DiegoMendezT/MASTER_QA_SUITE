"""
Test: Element Locators and Basic Interactions
Selenium/API Features: [find_element(By.ID), find_element(By.CSS_SELECTOR), find_element(By.XPATH), .click()]
AUT: The Internet
Markers: @ui
Purpose: To demonstrate finding elements using different locator strategies (ID, CSS, XPath) and performing a basic click action. This is a fundamental skill for UI automation.
"""
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.ui
def test_02_locators_and_clicks(driver):
    """
    Tests finding elements by various locators and clicking on them.
    """
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    # Arrange: Navigate to the "Add/Remove Elements" page
    driver.get(config['urls']['the_internet'] + "/add_remove_elements/")

    # Act & Assert 1: Find button by CSS Selector and click
    add_element_button_css = driver.find_element(By.CSS_SELECTOR, "button[onclick='addElement()']")
    add_element_button_css.click()

    # Assert that a new element was added
    delete_button_css = driver.find_element(By.CSS_SELECTOR, ".added-manually")
    assert delete_button_css.is_displayed(), "Element should be added after clicking 'Add Element'"
    
    # Act & Assert 2: Find the same button by XPath and click again
    add_element_button_xpath = driver.find_element(By.XPATH, "//button[text()='Add Element']")
    add_element_button_xpath.click()

    # Assert that a second element was added
    delete_buttons = driver.find_elements(By.CSS_SELECTOR, ".added-manually")
    assert len(delete_buttons) == 2, "There should be two 'Delete' buttons after clicking twice."

    # Act & Assert 3: Click the first delete button
    delete_buttons[0].click()
    
    # Assert that one element was removed
    remaining_buttons = driver.find_elements(By.CSS_SELECTOR, ".added-manually")
    assert len(remaining_buttons) == 1, "There should be one 'Delete' button remaining."
