
# Lesson: Test Google

Google search test - First validation test for MASTER QA SUITE v2.0

---

## Test Implementation

```python
"""
Google search test - First validation test for MASTER QA SUITE v2.0
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage

class GooglePage(BasePage):
    """Google search page object"""
    
    # Locators
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    RESULTS_CONTAINER = (By.ID, "search")
    FIRST_RESULT = (By.CSS_SELECTOR, "h3")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.google.com"
    
    def navigate(self):
        """Navigate to Google homepage"""
        self.driver.get(self.url)
    
    def search(self, query):
        """Perform search with given query"""
        self.enter_text(self.SEARCH_BOX, query)
        search_box = self.find_element(self.SEARCH_BOX)
        search_box.send_keys(Keys.RETURN)
    
    def is_results_displayed(self):
        """Check if search results are displayed"""
        return self.is_element_visible(self.RESULTS_CONTAINER)
    
    def get_first_result_text(self):
        """Get text of first search result"""
        return self.get_text(self.FIRST_RESULT)

@pytest.mark.smoke
@pytest.mark.ui
class TestGoogleSearch:
    """Google search test cases"""
    
    def test_google_search_selenium(self, driver, config):
        """Test Google search functionality"""
        # Arrange
        google_page = GooglePage(driver)
        search_query = "Selenium WebDriver"
        
        # Act
        google_page.navigate()
        google_page.search(search_query)
        
        # Assert
        assert google_page.is_results_displayed(), "Search results should be displayed"
        assert google_page.wait_for_url_contains("search"), "URL should contain 'search'"
        
        first_result = google_page.get_first_result_text()
        assert first_result, "First result should have text"
        print(f"First result: {first_result}")
    
    def test_google_title(self, driver):
        """Test Google homepage title"""
        # Arrange
        google_page = GooglePage(driver)
        
        # Act
        google_page.navigate()
        
        # Assert
        title = google_page.get_page_title()
        assert "Google" in title, f"Page title should contain 'Google', got: {title}"
    
    @pytest.mark.slow
    def test_google_search_multiple_queries(self, driver):
        """Test multiple search queries"""
        google_page = GooglePage(driver)
        queries = ["Python", "JavaScript", "Selenium", "Pytest"]
        
        for query in queries:
            google_page.navigate()
            google_page.search(query)
            assert google_page.is_results_displayed(), f"Results should display for: {query}"
            print(f"✅ Search successful for: {query}")

```

---

## Traceability

- **Test File**: `tests\test_google.py`
- **Markers**: ``@slow`, `@smoke`, `@ui``
