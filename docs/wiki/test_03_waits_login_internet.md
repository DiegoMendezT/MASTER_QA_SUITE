
# Lesson: Test 03 Waits Login Internet

Test: Explicit Waits
Selenium/API Features: [WebDriverWait, EC.visibility_of_element_located]
AUT: The Internet
Markers: @ui
Purpose: To demonstrate the use of explicit waits (WebDriverWait) to handle dynamic elements that may not be immediately present on the page. This is a critical technique for avoiding flaky tests.

---

## Test Implementation

```python
"""
Test: Explicit Waits
Selenium/API Features: [WebDriverWait, EC.visibility_of_element_located]
AUT: The Internet
Markers: @ui
Purpose: To demonstrate the use of explicit waits (WebDriverWait) to handle dynamic elements that may not be immediately present on the page. This is a critical technique for avoiding flaky tests.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.ui
def test_03_explicit_waits_for_dynamic_element(driver, config):
    """
    Tests waiting for a dynamically loaded element to appear.
    """
    # Arrange: Navigate to the "Dynamic Loading" example page
    driver.get(config['urls']['the_internet'] + "/dynamic_loading/2")

    # Act: Click the "Start" button to trigger the loading of a new element
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    start_button.click()

    # Assert: Use WebDriverWait to wait for the "Hello World!" text to be visible
    # This is the key part of the test. We wait up to 10 seconds for the element.
    wait = WebDriverWait(driver, 10)
    finish_element = wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    # Verify the text of the element that appeared
    assert "Hello World!" in finish_element.text, "The expected 'Hello World!' text was not found."

```

---

## Traceability

- **Test File**: `tests\ui\test_03_waits_login_internet.py`
- **Markers**: ``@ui``
