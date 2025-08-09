"""
Page Object for the Sauce Demo Login Page.

This class encapsulates the elements and actions available on the login page
of the Sauce Demo application (https://www.saucedemo.com).
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SauceLoginPage(BasePage):
    """
    Represents the login page and its interactions.
    """
    # --- Locators ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver, config):
        """
        Initializes the SauceLoginPage.
        """
        super().__init__(driver, config)
        self.url = self.config['urls']['sauce_demo']

    def load(self):
        """
        Navigates to the Sauce Demo login page.
        """
        self.go_to_url(self.url)

    def login(self, username, password):
        """
        Performs the login action.
        
        Args:
            username: The username to enter.
            password: The password to enter.
        """
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """
        Gets the text of the login error message.
        
        Returns:
            The error message text as a string.
        """
        return self.get_element_text(self.ERROR_MESSAGE)
