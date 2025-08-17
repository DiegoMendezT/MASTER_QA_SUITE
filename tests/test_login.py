"""
Login test scenarios for MASTER QA SUITE v2.0
Demonstrates advanced form testing, data generation, and POM reuse
"""
import logging

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from utils.data_factory import DataFactory

logger = logging.getLogger(__name__)

@pytest.mark.smoke
@pytest.mark.ui
class TestLoginScenarios:
    @staticmethod
    def _is_site_reachable(host="the-internet.herokuapp.com", port=443, timeout=3):
        import socket
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False
    """Comprehensive login testing scenarios"""
    
    def test_invalid_login_with_fake_data(self, driver, config):
    # xfail removed: test now passes reliably
        """Test login with invalid credentials using generated data"""
        # Test with the-internet.herokuapp.com login page (reliable test site)
        login_url = "https://the-internet.herokuapp.com/login"
        login_page = LoginPage(driver, config)
        
        # Navigate to login page
        driver.get(login_url)
        
        # Generate fake credentials
        fake_username = DataFactory.random_string(8)
        fake_password = DataFactory.random_password(12)
        
        logger.info(f"Testing with fake username: {fake_username}")
        
        # Perform login with fake data
        # Note: the-internet uses different locators
        driver.find_element(By.ID, "username").send_keys(fake_username)
        driver.find_element(By.ID, "password").send_keys(fake_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify error message appears
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        error_text = error_element.text
        
        assert "invalid" in error_text.lower() or "incorrect" in error_text.lower(), \
            f"Expected error message for invalid login, got: {error_text}"
        
        logger.info(f"✅ Invalid login properly rejected with message: {error_text}")
    
    def test_valid_login_the_internet(self, driver):
    # xfail removed: test now passes reliably
        """Test valid login on the-internet.herokuapp.com"""
        login_url = "https://the-internet.herokuapp.com/login"
        driver.get(login_url)
        
        # Valid credentials for the-internet.herokuapp.com
        valid_username = "tomsmith"
        valid_password = "SuperSecretPassword!"
        
        # Perform login
        driver.find_element(By.ID, "username").send_keys(valid_username)
        driver.find_element(By.ID, "password").send_keys(valid_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify successful login
        wait = WebDriverWait(driver, 10)
        success_element = wait.until(EC.presence_of_element_located((By.ID, "flash")))
        success_message = success_element.text
        assert "secure area" in success_message.lower(), \
            f"Expected success message, got: {success_message}"
        
        # Verify URL changed to secure area
        assert "/secure" in driver.current_url, \
            f"Expected redirect to secure area, current URL: {driver.current_url}"
        
        logger.info("✅ Valid login successful - redirected to secure area")
    
    def test_empty_credentials(self, driver):
    # xfail removed: test now passes reliably
        """Test login with empty credentials"""
        login_url = "https://the-internet.herokuapp.com/login"
        driver.get(login_url)
        
        # Try login with empty fields
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Should show error for empty username
        error_element = driver.find_element(By.ID, "flash")
        error_text = error_element.text
        
        assert "invalid" in error_text.lower(), \
            f"Expected error for empty credentials, got: {error_text}"
        
        logger.info("✅ Empty credentials properly rejected")
    
    def test_only_username_provided(self, driver):
    # xfail removed: test now passes reliably
        """Test login with only username, no password"""
        login_url = "https://the-internet.herokuapp.com/login"
        driver.get(login_url)

        # Enter only username
        username = DataFactory.random_string(8)
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for error element
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        error_text = error_element.text

        assert "invalid" in error_text.lower(), \
            f"Expected error for missing password, got: {error_text}"

        logger.info("✅ Missing password properly handled")
    
    @pytest.mark.slow
    def test_multiple_invalid_attempts(self, driver):
        # xfail removed: test now passes reliably
        """Test multiple invalid login attempts"""
        login_url = "https://the-internet.herokuapp.com/login"
        
        attempts = [
            ("admin", "admin"),
            ("user", "password"),
            ("test", "test123"),
            (DataFactory.random_email(), DataFactory.random_password())
        ]
        
        for username, password in attempts:
            driver.get(login_url)  # Fresh page for each attempt
            
            driver.find_element(By.ID, "username").send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password) 
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Verify each attempt fails
            error_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "flash"))
            )
            error_text = error_element.text
            
            assert "invalid" in error_text.lower(), \
                f"Expected error for {username}:{password}, got: {error_text}"
            
            logger.info(f"✅ Invalid attempt properly rejected: {username}")
    
    def test_login_page_elements_present(self, driver):
    # xfail removed: test now passes reliably
        """Test that all expected login page elements are present"""
        login_url = "https://the-internet.herokuapp.com/login"
        driver.get(login_url)
        
        # Verify form elements exist
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Verify elements are interactable
        assert username_field.is_enabled(), "Username field should be enabled"
        assert password_field.is_enabled(), "Password field should be enabled" 
        assert login_button.is_enabled(), "Login button should be enabled"
        
        # Verify placeholders or labels
        assert username_field.get_attribute("type") == "text", "Username should be text input"
        assert password_field.get_attribute("type") == "password", "Password should be password input"
        
        logger.info("✅ All login page elements present and functional")
    
    def test_password_masking(self, driver):
        # xfail removed: test now passes reliably
        """Test that password field masks input"""
        login_url = "https://the-internet.herokuapp.com/login"
        driver.get(login_url)

        password_field = driver.find_element(By.ID, "password")
        test_password = "TestPassword123!"

        password_field.send_keys(test_password)

        # Password field should be type="password" to mask input
        field_type = password_field.get_attribute("type")
        assert field_type == "password", f"Password field should mask input, type is: {field_type}"

        logger.info("✅ Password field properly masks input")

def _is_site_reachable(host):
    import socket
    try:
        socket.setdefaulttimeout(3)
        socket.gethostbyname(host)
        s = socket.create_connection((host, 80), 3)
        s.close()
        return True
    except Exception:
        return False
    
@pytest.mark.regression
class TestLoginPageNavigation:
    """Test navigation and page behavior"""
    
    @staticmethod
    def _is_site_reachable(host="the-internet.herokuapp.com", port=443, timeout=3):
        import socket
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False

    def test_login_page_title(self, driver):
        if not self._is_site_reachable():
            pytest.xfail("the-internet.herokuapp.com is unreachable; test skipped for CI reliability.")
        """Test login page has correct title"""
        driver.get("https://the-internet.herokuapp.com/login")
        
        WebDriverWait(driver, 10).until(EC.title_contains("The Internet"))
        title = driver.title
        assert "The Internet" in title, f"Expected 'The Internet' in title, got: {title}"
        
        logger.info(f"✅ Login page title verified: {title}")
    
    def test_successful_login_redirect(self, driver):
        if not self._is_site_reachable():
            pytest.xfail("the-internet.herokuapp.com is unreachable; test skipped for CI reliability.")
        """Test successful login redirects to correct page"""
        driver.get("https://the-internet.herokuapp.com/login")
        
        # Valid login
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Check redirect
        WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
        current_url = driver.current_url
        assert "/secure" in current_url, f"Should redirect to secure area, got: {current_url}"
        
        # Verify secure page content
        secure_area_text = driver.find_element(By.TAG_NAME, "h2").text
        assert "Secure Area" in secure_area_text, "Should show secure area heading"
        
        logger.info("✅ Login redirect behavior verified")
