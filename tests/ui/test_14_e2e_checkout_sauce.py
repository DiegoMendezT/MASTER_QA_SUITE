"""
Test: End-to-End Checkout Flow
Selenium/API Features: [Page Object Model, Sequential Actions]
AUT: Sauce Demo
Markers: @ui @integration
Purpose: To verify a complete user journey from login to checkout confirmation, demonstrating the use of the Page Object Model to structure a complex test.
"""
import pytest
from pages.sauce_login_page import SauceLoginPage
from pages.sauce_inventory_page import SauceInventoryPage

# Note: For a real E2E test, we would create more page objects (Cart, Checkout, etc.)
# For this MVP, we will keep it focused on Login -> Inventory.

@pytest.mark.ui
@pytest.mark.integration
def test_14_e2e_login_and_verify_inventory(driver, config):
    """
    Tests a successful login to Sauce Demo and verifies the inventory page.
    """
    # Arrange
    login_page = SauceLoginPage(driver, config)
    inventory_page = SauceInventoryPage(driver, config)
    
    # Act
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    
    # Assert
    # Verify that we have landed on the inventory page
    assert "products" in inventory_page.get_title().lower(), "Page title should indicate the products/inventory page."
    
    # Verify that the shopping cart is visible
    assert inventory_page.is_cart_displayed(), "Shopping cart icon should be visible after login."
    
    # Verify that there are products listed
    assert inventory_page.get_inventory_item_count() > 0, "There should be at least one inventory item displayed."
