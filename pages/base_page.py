"""
Base Page for all Page Objects

This class contains common methods that are used across multiple pages,
such as navigating to a URL, finding elements, and interacting with them.
All other page object classes will inherit from this class.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class BasePage:
    """
    The foundation for all page objects in the suite.
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
        # Provide a default for implicit_wait if config is empty
        wait_time = self.config.get('selenium', {}).get('implicit_wait', 10)
        self.wait = WebDriverWait(self.driver, wait_time)
        self.wait_timeout = int(self.config.get("wait_timeout", 10))

    def go_to_url(self, url):
        """Navigates the browser to the specified URL."""
        self.driver.get(url)

    def open(self, url=None):
        """Navigates to a URL, preferring the one provided, or falling back to a base_url from config."""
        # Determine base_url from config, default to an empty string if not found
        base_url = self.config.get("base_url", "")
        target_url = url or base_url
        if not target_url:
            raise ValueError("No URL provided and no 'base_url' found in configuration.")
        self.driver.get(target_url)

    def find_element(self, by_locator):
        """
        Finds and returns a single element, waiting for it to be visible.
        
        Args:
            by_locator: A tuple containing the locator strategy and value (e.g., (By.ID, 'element_id')).
        
        Returns:
            The WebElement object.
        """
        return self.wait.until(EC.visibility_of_element_located(by_locator))

    def find_elements(self, by_locator):
        """
        Finds and returns a list of elements, waiting for them to be visible.

        Args:
            by_locator: A tuple containing the locator strategy and value.

        Returns:
            A list of WebElement objects.
        """
        return self.wait.until(EC.visibility_of_all_elements_located(by_locator))

    def click(self, by_locator, timeout=None):
        """
        Waits for an element to be clickable and then clicks it.
        If the standard click is intercepted, it falls back to a JavaScript click.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
        """
        wait_time = timeout or self.wait_timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(by_locator)
            )
            element.click()
        except (TimeoutException, ElementClickInterceptedException):
            try:
                # Fallback to JavaScript click if the element is not clickable
                # (e.g., obscured by another element)
                element = self.find_element(by_locator) # Wait for presence
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as js_e:
                # If the JS click also fails, raise an informative error
                raise Exception(f"Failed to click {by_locator} with standard and JS click. JS click error: {js_e}")

    def enter_text(self, by_locator, text, clear=True, timeout=None):
        """
        Finds an element, clears its content, and enters the given text.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            text: The text to enter into the element.
        """
        el = WebDriverWait(self.driver, timeout or self.wait_timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        if clear:
            try:
                el.clear()
            except Exception:
                pass  # Ignore errors on clear, e.g., on non-input elements
        el.send_keys(text)

    def get_element_text(self, by_locator, timeout=None):
        """
        Finds an element and returns its text content.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            
        Returns:
            The text of the element as a string.
        """
        el = WebDriverWait(self.driver, timeout or self.wait_timeout).until(
            EC.visibility_of_element_located(by_locator)
        )
        return el.text

    def get_text(self, by_locator, timeout=None):
        """Alias for get_element_text for brevity."""
        return self.get_element_text(by_locator, timeout)

    def is_element_visible(self, by_locator, timeout=None):
        """
        Checks if an element is visible on the page.
        
        Args:
            by_locator: A tuple containing the locator strategy and value.
            timeout: The maximum time to wait for the element.
            
        Returns:
            True if the element is visible, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout or self.wait_timeout).until(
                EC.visibility_of_element_located(by_locator)
            )
            return True
        except TimeoutException:
            return False

    def get_page_title(self):
        """Returns the title of the current page."""
        return self.driver.title

    def wait_for_url_contains(self, substring, timeout=None):
        """
        Waits for the URL to contain a specific substring.
        
        Args:
            substring: The substring to look for in the URL.
            timeout: The maximum time to wait.
            
        Returns:
            True if the URL contains the substring, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout or self.wait_timeout).until(EC.url_contains(substring))
            return True
        except TimeoutException:
            return False

