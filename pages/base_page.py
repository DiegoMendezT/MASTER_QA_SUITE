# pages/base_page.py
"""
Base Page for all Page Objects

This class contains common methods that are used across multiple pages,
such as navigating to a URL, finding elements, and interacting with them.
All other page object classes will inherit from this class.
"""
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.exceptions import (ElementInteractionException,
                              ElementNotFoundException)
from utils.flaky_guard import FlakyGuard

# Set up a logger for the base page
logger = logging.getLogger(__name__)

# Apply the FlakyGuard to the entire BasePage class.
# This will automatically retry all public methods on transient errors.
@FlakyGuard(retries=3, backoff=0.5)
class BasePage:
    """
    The foundation for all page objects in the suite.
    Includes robust error handling, logging, and automatic retry via FlakyGuard.
    """
    def __init__(self, driver, config=None, **_):
        """
        Initializes the BasePage with a WebDriver instance and configuration.
        
        Args:
            driver: The Selenium WebDriver instance.
            config: The configuration dictionary loaded from settings.yaml.
        """
        self.driver = driver
        self.config = config or {}
        # Use a shorter wait time for individual checks, as FlakyGuard will handle retries.
        wait_time = self.config.get('selenium', {}).get('explicit_wait', 5)
        self.wait = WebDriverWait(self.driver, wait_time)

    def go_to_url(self, url):
        """Navigates the browser to the specified URL."""
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def open(self, url=None):
        """Navigates to a URL, preferring the one provided, or falling back to a base_url from config."""
        base_url = self.config.get("base_url", "")
        target_url = url or base_url
        if not target_url:
            raise ValueError("No URL provided and no 'base_url' found in configuration.")
        logger.info(f"Opening page: {target_url}")
        self.driver.get(target_url)

    def find_element(self, by_locator):
        """
        Finds and returns a single element, waiting for it to be visible.
        The FlakyGuard decorator handles retries on failure.
        
        Args:
            by_locator: A tuple containing the locator strategy and value (e.g., (By.ID, 'element_id')).
        
        Returns:
            The WebElement object.
            
        Raises:
            ElementNotFoundException: If the element is not found after all retries.
        """
        logger.debug(f"Finding element by {by_locator}")
        try:
            return self.wait.until(EC.visibility_of_element_located(by_locator))
        except TimeoutException:
            msg = f"Element not found or not visible after retries: {by_locator}"
            logger.error(msg)
            # Take a screenshot on final failure for debugging
            self.driver.save_screenshot(f"error_find_element_{by_locator[1]}.png")
            raise ElementNotFoundException(msg)

    def find_elements(self, by_locator):
        """
        Finds and returns a list of elements, waiting for them to be visible.
        The FlakyGuard decorator handles retries on failure.

        Args:
            by_locator: A tuple containing the locator strategy and value.

        Returns:
            A list of WebElement objects.
            
        Raises:
            ElementNotFoundException: If no elements are found after all retries.
        """
        logger.debug(f"Finding elements by {by_locator}")
        try:
            return self.wait.until(EC.visibility_of_all_elements_located(by_locator))
        except TimeoutException:
            msg = f"Elements not found or not visible after retries: {by_locator}"
            logger.error(msg)
            self.driver.save_screenshot(f"error_find_elements_{by_locator[1]}.png")
            raise ElementNotFoundException(msg)

    def click(self, by_locator):
        """
        Waits for an element to be clickable and then clicks it.
        The FlakyGuard decorator handles retries on failure.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            
        Raises:
            ElementInteractionException: If the element cannot be clicked after all retries.
        """
        logger.info(f"Clicking element: {by_locator}")
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            # Attempt a robust JS click as a primary method
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            msg = f"Failed to click {by_locator} after retries. Final error: {e}"
            logger.error(msg)
            self.driver.save_screenshot(f"error_click_{by_locator[1]}.png")
            raise ElementInteractionException(msg)

    def enter_text(self, by_locator, text, clear=True):
        """
        Finds an element, clears its content, and enters the given text.
        The FlakyGuard decorator handles retries on failure.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            text: The text to enter into the element.
            clear: Whether to clear the field before entering text.
            
        Raises:
            ElementInteractionException: If text cannot be entered after all retries.
        """
        logger.info(f"Entering text '{text}' into element: {by_locator}")
        try:
            element = self.find_element(by_locator)
            if clear:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            msg = f"Failed to enter text in {by_locator} after retries. Error: {e}"
            logger.error(msg)
            self.driver.save_screenshot(f"error_enter_text_{by_locator[1]}.png")
            raise ElementInteractionException(msg)

    def get_element_text(self, by_locator):
        """

        Finds an element and returns its text content.
        The FlakyGuard decorator handles retries on failure.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            
        Returns:
            The text of the element as a string.
        """
        logger.debug(f"Getting text from element: {by_locator}")
        element = self.find_element(by_locator)
        return element.text

    def is_element_visible(self, by_locator, timeout=None):
        """
        Checks if an element is visible on the page within a specified timeout.
        Note: This method is not typically retried by FlakyGuard unless it fails
        with a handled exception, as it's intended to be a check.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            timeout: The maximum time to wait for the element. Defaults to the default wait time.
            
        Returns:
            True if the element is visible, False otherwise.
        """
        logger.debug(f"Checking visibility of element: {by_locator}")
        # Use a custom wait time if provided, otherwise the default explicit wait
        wait_time = timeout if timeout is not None else self.wait._timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(by_locator)
            )
            return True
        except TimeoutException:
            return False

    def get_page_title(self):
        """Returns the title of the current page."""
        title = self.driver.title
        logger.info(f"Current page title: {title}")
        return title

    def wait_for_url_contains(self, substring, timeout=None):
        """
        Waits for the URL to contain a specific substring.
        
        Args:
            substring: The substring to look for in the URL.
            timeout: The maximum time to wait. Defaults to the default wait time.
            
        Returns:
            True if the URL contains the substring within the timeout, False otherwise.
        """
        wait_time = timeout if timeout is not None else self.wait._timeout
        logger.info(f"Waiting for URL to contain: '{substring}'")
        try:
            # Use a specific WebDriverWait for this check
            WebDriverWait(self.driver, wait_time).until(EC.url_contains(substring))
            return True
        except TimeoutException:
            logger.warning(f"Timeout waiting for URL to contain '{substring}'. Current URL: {self.driver.current_url}")
            return False

