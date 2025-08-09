"""
Google search test - First validation test for MASTER QA SUITE v2.0
"""
import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

class GooglePage(BasePage):
    SEARCH_BOX = (By.NAME, "q")
    RESULTS_CONTAINER = (By.ID, "search")  # stable-ish

    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.url = "https://www.google.com/ncr"  # /ncr avoids country redirect

    def open_home(self):
        self.open(self.url)
        self._dismiss_consent_if_present()

    def _dismiss_consent_if_present(self):
        # Handle possible consent dialog variants; ignore if not present
        selectors = [
            (By.CSS_SELECTOR, "button[aria-label*='Accept']"),
            (By.ID, "L2AGLb"),
            (By.XPATH, "//button[div[contains(text(), 'Accept all')]]"),
        ]
        for sel in selectors:
            try:
                if self.is_element_visible(sel, timeout=3):
                    self.click(sel, timeout=3)
                    break
            except TimeoutException:
                pass

    def search(self, query):
        self.enter_text(self.SEARCH_BOX, query)
        from selenium.webdriver.common.keys import Keys
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)
        self.wait_for_url_contains("search?")

    def is_results_displayed(self):
        return self.is_element_visible(self.RESULTS_CONTAINER, timeout=15)

@pytest.mark.ui
@pytest.mark.external  # optional: these can be flaky due to consent/captchas
def test_google_title(driver, config):
    google = GooglePage(driver, config)
    google.open_home()
    assert "Google" in google.get_page_title()

@pytest.mark.ui
@pytest.mark.external
def test_google_search_selenium(driver, config):
    google = GooglePage(driver, config)
    google.open_home()
    google.search("selenium webdriver")
    assert google.is_results_displayed(), "Search results should be displayed"

@pytest.mark.ui
@pytest.mark.external
@pytest.mark.parametrize("query", ["python", "pytest", "selenium"])
def test_google_search_multiple_queries(driver, config, query):
    google = GooglePage(driver, config)
    google.open_home()
    google.search(query)
    assert google.is_results_displayed(), f"Results should display for: {query}"
