"""
Login Page Object Model for MASTER QA SUITE v2.0
Demonstrates advanced form handling and POM inheritance
"""
import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Login page object with form interactions and validation"""
    
    # Locators for different login page patterns
    USERNAME_INPUT = (By.ID, "username")
    USERNAME_INPUT_ALT = (By.NAME, "username") 
    USERNAME_INPUT_EMAIL = (By.ID, "email")
    
    PASSWORD_INPUT = (By.ID, "password")
    PASSWORD_INPUT_ALT = (By.NAME, "password")
    
    LOGIN_BUTTON = (By.ID, "login")
    LOGIN_BUTTON_ALT = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_BUTTON_TEXT = (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
    
    ERROR_MESSAGE = (By.CLASS_NAME, "error")
    ERROR_MESSAGE_ALT = (By.ID, "error")
    ERROR_MESSAGE_XPATH = (By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'alert')]")
    
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.url_pattern = "/login"
    
    def navigate_to_login(self, base_url):
        """Navigate to login page"""
        login_url = base_url.rstrip('/') + self.url_pattern
        self.driver.get(login_url)
        logger.info(f"Navigated to login page: {login_url}")
    
    def enter_username(self, username):
        """Enter username with fallback locators"""
        locators = [self.USERNAME_INPUT, self.USERNAME_INPUT_ALT, self.USERNAME_INPUT_EMAIL]
        
        for locator in locators:
            try:
                self.enter_text(locator, username, timeout=5)
                logger.info(f"Username entered using locator: {locator}")
                return True
            except TimeoutException:
                continue
        
        raise Exception("Could not find username input field with any known locator")
    
    def enter_password(self, password):
        """Enter password with fallback locators"""
        locators = [self.PASSWORD_INPUT, self.PASSWORD_INPUT_ALT]
        
        for locator in locators:
            try:
                self.enter_text(locator, password, timeout=5)
                logger.info(f"Password entered using locator: {locator}")
                return True
            except TimeoutException:
                continue
        
        raise Exception("Could not find password input field with any known locator")
    
    def click_login_button(self):
        """Click login button with fallback locators"""
        locators = [self.LOGIN_BUTTON, self.LOGIN_BUTTON_ALT, self.LOGIN_BUTTON_TEXT]
        
        for locator in locators:
            try:
                self.click_element(locator, timeout=5)
                logger.info(f"Login button clicked using locator: {locator}")
                return True
            except TimeoutException:
                continue
        
        raise Exception("Could not find login button with any known locator")
    
    def perform_login(self, username, password):
        """Complete login flow"""
        try:
            self.enter_username(username)
            self.enter_password(password)
            self.click_login_button()
            logger.info(f"Login attempted with username: {username}")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
    
    def get_error_message(self):
        """Get error message with multiple fallback locators"""
        locators = [self.ERROR_MESSAGE, self.ERROR_MESSAGE_ALT, self.ERROR_MESSAGE_XPATH]
        
        for locator in locators:
            try:
                error_text = self.get_text(locator, timeout=5)
                if error_text:
                    logger.info(f"Error message found: {error_text}")
                    return error_text
            except TimeoutException:
                continue
        
        return ""
    
    def is_error_displayed(self):
        """Check if error message is visible"""
        locators = [self.ERROR_MESSAGE, self.ERROR_MESSAGE_ALT, self.ERROR_MESSAGE_XPATH]
        
        for locator in locators:
            if self.is_element_visible(locator, timeout=3):
                return True
        return False
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.click_element(self.FORGOT_PASSWORD_LINK)
        logger.info("Clicked forgot password link")
    
    def click_register_link(self):
        """Click register link"""
        self.click_element(self.REGISTER_LINK)
        logger.info("Clicked register link")
    
    def is_login_form_visible(self):
        """Check if login form is loaded and visible"""
        username_visible = (self.is_element_visible(self.USERNAME_INPUT, timeout=5) or 
                          self.is_element_visible(self.USERNAME_INPUT_ALT, timeout=2) or
                          self.is_element_visible(self.USERNAME_INPUT_EMAIL, timeout=2))
        
        password_visible = (self.is_element_visible(self.PASSWORD_INPUT, timeout=5) or
                          self.is_element_visible(self.PASSWORD_INPUT_ALT, timeout=2))
        
        return username_visible and password_visible
    
    def wait_for_redirect_after_login(self, expected_url_fragment, timeout=10):
        """Wait for redirect after successful login"""
        return self.wait_for_url_contains(expected_url_fragment, timeout)
