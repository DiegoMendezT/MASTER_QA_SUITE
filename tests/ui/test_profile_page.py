"""
Test suite for the User Profile (Inventory) Page.
"""
import pytest
import os
from pages.profile_page import ProfilePage

def save_ui_screenshot(driver, name):
    screenshot_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'artifacts', 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    return screenshot_path


@pytest.mark.ui
@pytest.mark.profile
class TestProfilePage:
    """
    Contains tests for the main user profile/inventory page.
    """

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver, config):
        """
        Setup fixture to initialize the page object for each test.
        """
        self.driver = logged_in_driver
        self.config = config
        self.profile_page = ProfilePage(self.driver, self.config)

    def test_inventory_is_displayed_after_login(self):
        """
        Verifies that the inventory container is visible after a successful login.
        """
        save_ui_screenshot(self.driver, "test_profile_inventory_displayed")
        assert self.profile_page.is_inventory_displayed(), "Inventory container should be visible after login."

    def test_page_title_is_correct(self):
        """
        Verifies that the page title is "Products".
        """
        expected_title = "Products"
        actual_title = self.profile_page.get_page_title()
        save_ui_screenshot(self.driver, "test_profile_page_title")
        assert actual_title == expected_title, f"Page title should be '{expected_title}', but was '{actual_title}'."

    def test_default_sort_option_is_name_az(self):
        """
        Verifies that the default product sort option is "Name (A to Z)".
        """
        expected_sort = "Name (A to Z)"
        active_sort = self.profile_page.get_active_sort_option()
        save_ui_screenshot(self.driver, "test_profile_default_sort_option")
        assert expected_sort in active_sort, f"Default sort option should be '{expected_sort}'."

    def test_shopping_cart_link_is_functional(self):
        """
        Verifies that clicking the shopping cart icon navigates to the cart page.
        """
        self.profile_page.click_shopping_cart()
        save_ui_screenshot(self.driver, "test_profile_cart_link")
        assert self.profile_page.wait_for_url_contains("cart.html"), "Should navigate to the cart page."
