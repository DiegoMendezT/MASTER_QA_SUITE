"""
Pytest configuration and fixtures for MASTER QA SUITE v2.0
"""
import logging
import os
import shutil
import tempfile
import threading

import allure
import pytest
import yaml
from allure_commons.types import AttachmentType
from applitools.selenium import BatchInfo, Configuration, Eyes, Target
from chromedriver_autoinstaller import install
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-local storage for resources that need to be unique per thread/worker
thread_local_data = threading.local()

# --- Constants ---
SAUCE_ENABLED = bool(os.getenv("SAUCE_USERNAME") and os.getenv("SAUCE_ACCESS_KEY"))

# --- Playwright/Selenium engine toggle ---------------------------
def pytest_addoption(parser):
    """Add custom command-line options to pytest."""
    group = parser.getgroup("engine", "Engine Configuration")
    group.addoption(
        "--engine",
        action="store",
        default="selenium",
        choices=["selenium", "playwright"],
        help="Choose test engine: selenium | playwright (default: selenium)",
    )
    
    # Selenium-specific browser option
    group.addoption(
        "--sel-browser",
        action="store",
        default="chrome",
        help="Choose Selenium browser: chrome | firefox | edge (default: chrome)",
    )

    # Let pytest-playwright handle its own options like --browser, --headed etc.
    
    # Add other options to the general group to avoid conflicts
    parser.addoption(
        "--integration-mode", 
        action="store", 
        default=None, 
        help="Mode for integration tests: 'simulated' or 'live'"
    )
    parser.addoption(
        "--login-mode", 
        action="store", 
        default="UI Login", 
        help="Login method: 'UI Login' or 'API+Cookie Login'"
    )

def pytest_configure(config):
    # Make the selected engine visible in reports/metadata
    config._metadata = getattr(config, "_metadata", {})
    config._metadata["Engine"] = config.getoption("--engine")
    if config.getoption("--engine") == "playwright":
        # For Playwright, browser and headed are standard pytest-playwright options
        config._metadata["PW Browser"] = config.getoption("browser")
        config._metadata["PW Headed"] = config.getoption("--headed")


@pytest.fixture(scope="session")
def applitools_config():
    """Load Applitools configuration."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'applitools.yml')
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def integration_config():
    """Load integration configuration from integration.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'integration.yaml')
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="session")
def config():
    """Load configuration from settings.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yaml')
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

@pytest.fixture(scope="function")
def eyes(driver, applitools_config, request):
    """Applitools Eyes fixture for visual testing."""
    # Initialize the eyes SDK and set your private API key.
    api_key = os.getenv("APPLITOOLS_API_KEY", applitools_config.get('api_key'))
    if not api_key or "YOUR_APPLITOOLS_API_KEY" in api_key:
        pytest.skip("APPLITOOLS_API_KEY is not set or is a placeholder. Skipping visual tests.")

    eyes = Eyes()
    
    config = Configuration()
    config.set_api_key(api_key)
    config.set_batch(BatchInfo(applitools_config.get('batch_name', "MASTER QA SUITE")))
    config.set_app_name(applitools_config.get('app_name', "MASTER QA SUITE"))
    
    # Set viewport size
    vp_size = applitools_config.get('viewport_size', {'width': 1920, 'height': 1080})
    config.set_viewport_size({'width': vp_size['width'], 'height': vp_size['height']})

    eyes.set_configuration(config)
    
    # Start the test and set the browser's viewport size to match the baseline.
    eyes.open(driver, app_name=config.app_name, test_name=request.node.name)
    
    yield eyes
    
    # Close the eyes instance and abort if not closed.
    eyes.close_async()

@pytest.fixture(scope="function")
def driver(config, request):
    """
    WebDriver fixture that provides a driver instance for tests.
    - For local runs, it creates a fresh, isolated browser profile.
    - For CI/Sauce Labs runs, it connects to a remote WebDriver.
    - It is thread-safe for parallel execution.
    """
    # This fixture is for Selenium only. Playwright has its own fixtures.
    # We check if 'page' (a Playwright fixture) is in the request. If so, we skip.
    if 'page' in request.fixturenames:
        pytest.skip("Skipping Selenium driver fixture for a Playwright test.")
        return

    browser_name = request.config.getoption("--sel-browser").lower()
    
    if SAUCE_ENABLED:
        logging.info(f"Running on Sauce Labs with browser: {browser_name}")
        sauce_user = os.getenv("SAUCE_USERNAME")
        sauce_key = os.getenv("SAUCE_ACCESS_KEY")
        sauce_url = f"https://{sauce_user}:{sauce_key}@ondemand.saucelabs.com/wd/hub"
        
        sauce_options = {
            'build': f"master-qa-suite-build-{os.getenv('GITHUB_RUN_ID', 'local')}",
            'name': request.node.name
        }

        if browser_name == "firefox":
            from selenium.webdriver.firefox.options import \
                Options as FirefoxOptions
            options = FirefoxOptions()
            options.browser_version = 'latest'
            options.platform_name = 'Windows 11'
            options.set_capability('sauce:options', sauce_options)
        elif browser_name == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
            options.browser_version = 'latest'
            options.platform_name = 'Windows 11'
            options.set_capability('sauce:options', sauce_options)
        else: # Default to Chrome
            from selenium.webdriver.chrome.options import \
                Options as ChromeOptions
            options = ChromeOptions()
            options.browser_version = 'latest'
            options.platform_name = 'Windows 11'
            options.set_capability('sauce:options', sauce_options)

        web_driver = webdriver.Remote(command_executor=sauce_url, options=options)

    else: # Local execution
        logging.info(f"Running locally with browser: {browser_name}")
        if browser_name == "firefox":
            from selenium.webdriver.firefox.options import \
                Options as FirefoxOptions
            options = FirefoxOptions()
            web_driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
            web_driver = webdriver.Edge(options=options)
        else: # Default to local Chrome with hardened profile
            temp_profile_dir = tempfile.mkdtemp()
            
            try:
                install()
            except Exception as e:
                logging.error(f"Error installing ChromeDriver: {e}")
                pytest.fail("ChromeDriver installation failed.")

            options = Options()
            # Profile and Isolation
            options.add_argument(f"--user-data-dir={temp_profile_dir}")
            options.add_argument("--password-store=basic")
            options.add_argument("--incognito")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            # Disable Popups and Prompts
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-save-password-bubble")
            options.add_argument("--disable-features=PasswordManagerOnboarding,PasswordCheck,AutofillSaveCardPrompt")
            options.add_argument('--disable-blink-features=AutomationControlled')
            # Experimental options
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "autofill.profile_enabled": False,
                "download.default_directory": os.path.join(temp_profile_dir, "downloads"),
            })
            # General performance and stability
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument("--start-maximized")
            
            web_driver = webdriver.Chrome(options=options)
    
    yield web_driver

    # --- Teardown ---
    if SAUCE_ENABLED:
        sauce_result = "passed" if request.node.rep_call.passed else "failed"
        web_driver.execute_script(f"sauce:job-result={sauce_result}")

    web_driver.quit()
    
    if not SAUCE_ENABLED and browser_name == 'chrome':
        # Clean up the temporary profile directory for local chrome runs
        shutil.rmtree(options.arguments[0].split('=')[1], ignore_errors=True)


@pytest.fixture(scope="function")
def api_client(config):
    """
    Provides a thread-safe configured HTTP client for API tests.
    """
    if not hasattr(thread_local_data, "api_client"):
        from utils.http_client import get_http_client
        thread_local_data.api_client = get_http_client()
    return thread_local_data.api_client

@pytest.fixture(scope="session")
def integration_mode(request):
    """Returns the selected integration mode from the command line, defaulting to 'live'."""
    return request.config.getoption("--integration-mode") or "live"

@pytest.fixture(scope="function")
def active_integration_config(integration_mode, integration_config):
    """Returns the configuration for the active integration mode."""
    return integration_config[integration_mode]

@pytest.fixture(scope="function")
def logged_in_driver(driver, active_integration_config, config, request):
    """
    A driver instance that is already logged into the application.
    Can use either standard UI login or API+cookie injection based on --login-mode.
    """
    login_mode = request.config.getoption("--login-mode")
    base_url = active_integration_config['base_url']
    user = active_integration_config['user']
    password = active_integration_config['pass']

    if login_mode == "API+Cookie Login":
        logging.info("Using API+Cookie Login method.")
        # For SauceDemo, the cookie is simple. For a real app, this would
        # involve an API call to a login endpoint to get a session token.
        driver.get(base_url)  # Must visit the domain to set cookies for it
        driver.add_cookie({
            "name": "session-username",
            "value": user,
            "path": "/",
            "domain": "www.saucedemo.com"  # Domain must be correct
        })
        # After setting the cookie, go to the page that requires login
        inventory_url = f"{base_url.rstrip('/')}/inventory.html"
        driver.get(inventory_url)
    else:  # Default to "UI Login"
        logging.info("Using standard UI Login method.")
        from pages.sauce_login_page import SauceLoginPage
        login_page = SauceLoginPage(driver, config)
        driver.get(base_url)
        login_page.login(user, password)

    # A quick check to ensure login was successful
    assert "inventory.html" in driver.current_url, f"Login failed in logged_in_driver fixture using mode: {login_mode}"
    
    yield driver
    # Teardown (if any) can happen here, but the main driver fixture handles quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and report test status to Sauce Labs."""
    outcome = yield
    rep = outcome.get_result()
    
    # Store the result in the item for later use in the driver fixture
    if rep.when == "call":
        item.rep_call = rep

    if rep.when == "call" and rep.failed:
        try:
            # --- Screenshot and Allure attachment on failure ---
            if "driver" in item.fixturenames:
                web_driver = item.funcargs['driver']
                
                # Create a valid filename for the screenshot
                test_name = item.name.encode('ascii', 'ignore').decode('ascii').replace('[', '_').replace(']', '')
                screenshot_dir = os.path.join(os.path.dirname(__file__), 'artifacts', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_failed.png")
                
                # Save screenshot
                web_driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved: {screenshot_path}")

                # Attach to Allure report
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="failure_screenshot",
                    attachment_type=AttachmentType.PNG
                )
        except Exception as e:
            logging.error(f"Failed to capture screenshot or attach to Allure: {e}")

