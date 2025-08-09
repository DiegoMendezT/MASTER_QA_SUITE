"""
WebDriver Factory for MASTER QA SUITE v2.0
Handles Chrome, Firefox, Edge, and Remote (SauceLabs) drivers
"""
import os

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class WebDriverFactory:
    """Factory class for creating WebDriver instances"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
        
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def create_driver(self, browser="chrome", headless=False, remote_url=None):
        """Create WebDriver instance based on browser type"""
        
        if remote_url:
            return self._create_remote_driver(browser, remote_url)
        
        if browser.lower() == "chrome":
            return self._create_chrome_driver(headless)
        elif browser.lower() == "firefox":
            return self._create_firefox_driver(headless)
        elif browser.lower() == "edge":
            return self._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _create_chrome_driver(self, headless=False):
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        # Common Chrome options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        
        if headless:
            options.add_argument('--headless')
        
        # Window size from config
        window_size = self.config['browsers']['chrome']['window_size']
        options.add_argument(f'--window-size={window_size}')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Apply timeouts from config
        self._apply_timeouts(driver)
        return driver
    
    def _create_firefox_driver(self, headless=False):
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Window size from config
        width, height = self.config['browsers']['firefox']['window_size'].split(',')
        driver.set_window_size(int(width), int(height))
        
        self._apply_timeouts(driver)
        return driver
    
    def _create_edge_driver(self, headless=False):
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # Window size from config
        window_size = self.config['browsers']['edge']['window_size']
        options.add_argument(f'--window-size={window_size}')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        self._apply_timeouts(driver)
        return driver
    
    def _create_remote_driver(self, browser, remote_url):
        """Create Remote WebDriver for Selenium Grid or SauceLabs"""
        capabilities = self._get_capabilities(browser)
        
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=capabilities
        )
        
        self._apply_timeouts(driver)
        return driver
    
    def _get_capabilities(self, browser):
        """Get browser capabilities for remote execution"""
        capabilities_map = {
            "chrome": {
                "browserName": "chrome",
                "version": "latest",
                "platform": "ANY"
            },
            "firefox": {
                "browserName": "firefox",
                "version": "latest", 
                "platform": "ANY"
            },
            "edge": {
                "browserName": "MicrosoftEdge",
                "version": "latest",
                "platform": "ANY"
            }
        }
        
        return capabilities_map.get(browser.lower(), capabilities_map["chrome"])
    
    def _apply_timeouts(self, driver):
        """Apply timeout configurations to driver"""
        driver.implicitly_wait(self.config['selenium']['implicit_wait'])
        driver.set_page_load_timeout(self.config['selenium']['page_load_timeout'])
        driver.set_script_timeout(self.config['selenium']['script_timeout'])
        
        # Maximize window unless headless
        try:
            driver.maximize_window()
        except Exception:
            pass  # Headless mode might not support maximize
