"""
Element and selector validators for MASTER QA SUITE v2.0
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re

class Validator:
    """Utility class for validating elements and selectors"""
    
    @staticmethod
    def is_valid_locator(locator_tuple):
        """Validate if locator tuple is properly formatted"""
        if not isinstance(locator_tuple, tuple) or len(locator_tuple) != 2:
            return False
        
        by_type, locator_value = locator_tuple
        
        # Check if by_type is valid
        valid_by_types = [
            By.ID, By.NAME, By.CLASS_NAME, By.TAG_NAME,
            By.LINK_TEXT, By.PARTIAL_LINK_TEXT,
            By.CSS_SELECTOR, By.XPATH
        ]
        
        if by_type not in valid_by_types:
            return False
        
        # Check if locator_value is string and not empty
        if not isinstance(locator_value, str) or not locator_value.strip():
            return False
        
        return True
    
    @staticmethod
    def is_valid_xpath(xpath):
        """Validate XPath syntax"""
        try:
            # Basic XPath validation patterns
            if not xpath.startswith(('/', './/', '(')):
                return False
            
            # Check for common XPath syntax errors
            invalid_patterns = [
                r'///',  # Triple slash
                r'\[\]',  # Empty brackets
                r'\(\)',  # Empty parentheses without function
            ]
            
            for pattern in invalid_patterns:
                if re.search(pattern, xpath):
                    return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def is_valid_css_selector(css_selector):
        """Validate CSS selector syntax"""
        try:
            # Basic CSS selector validation
            if not css_selector.strip():
                return False
            
            # Check for common CSS selector errors
            invalid_patterns = [
                r'\.\.+',  # Multiple consecutive dots
                r'##',     # Multiple consecutive hashes
                r'\[\]',   # Empty attribute selector
            ]
            
            for pattern in invalid_patterns:
                if re.search(pattern, css_selector):
                    return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_element_present(driver, locator):
        """Check if element is present in DOM"""
        try:
            driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    @staticmethod
    def validate_element_visible(driver, locator):
        """Check if element is visible on page"""
        try:
            element = driver.find_element(*locator)
            return element.is_displayed()
        except (NoSuchElementException, Exception):
            return False
    
    @staticmethod
    def validate_element_clickable(driver, locator):
        """Check if element is clickable"""
        try:
            element = driver.find_element(*locator)
            return element.is_enabled() and element.is_displayed()
        except (NoSuchElementException, Exception):
            return False
    
    @staticmethod
    def validate_text_present(driver, text):
        """Check if text is present on page"""
        try:
            return text in driver.page_source
        except Exception:
            return False
    
    @staticmethod
    def validate_url_pattern(url, pattern):
        """Validate if URL matches expected pattern"""
        try:
            return bool(re.search(pattern, url))
        except Exception:
            return False
    
    @staticmethod
    def validate_email_format(email):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def validate_phone_format(phone):
        """Validate phone number format"""
        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        # Check if it's all digits and reasonable length
        return clean_phone.isdigit() and 10 <= len(clean_phone) <= 15
