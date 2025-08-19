
# Lesson: Test Homepage Visuals

Contains visual tests for the main pages of the application.

---

## Test Implementation

```python
import pytest
from applitools.selenium import Target


@pytest.mark.visual
@pytest.mark.usefixtures("logged_in_driver")
class TestHomepageVisuals:
    """
    Contains visual tests for the main pages of the application.
    """

    def test_inventory_page_looks_correct(self, eyes, driver):
        """
        This test validates the visual appearance of the main inventory page.
        It serves as a baseline for visual regression testing.
        """
        # Visual check of the entire window.
        eyes.check(Target.window().fully().with_name("Inventory Page"))

    def test_cart_page_looks_correct(self, eyes, driver):
        """
        This test validates the visual appearance of the cart page.
        """
        # For this test, let's navigate to the cart page first.
        # In a real scenario, you might add an item to the cart first.
        driver.get("https://www.saucedemo.com/cart.html")
        
        # Visual check of the cart page.
        eyes.check(Target.window().fully().with_name("Cart Page"))

```

---

## Traceability

- **Test File**: `tests\visual\test_homepage_visuals.py`
- **Markers**: ``@usefixtures`, `@visual``
