"""
Test suite for the User Profile (Inventory) Page.
"""
import pytest

from pages.profile_page import ProfilePage


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
        assert self.profile_page.is_inventory_displayed(), "Inventory container should be visible after login."

    def test_page_title_is_correct(self):
        """
        Verifies that the page title is "Products".
        """
        expected_title = "Products"
        actual_title = self.profile_page.get_page_title()
        assert actual_title == expected_title, f"Page title should be '{expected_title}', but was '{actual_title}'."

    def test_default_sort_option_is_name_az(self):
        """
        Verifies that the default product sort option is "Name (A to Z)".
        """
        # For Sauce Demo, the text includes all options. We check if the expected default is first.
        expected_sort = "Name (A to Z)"
        active_sort = self.profile_page.get_active_sort_option()
        assert expected_sort in active_sort, f"Default sort option should be '{expected_sort}'."

    def test_shopping_cart_link_is_functional(self):
        """
        Verifies that clicking the shopping cart icon navigates to the cart page.
        """
        self.profile_page.click_shopping_cart()
        assert self.profile_page.wait_for_url_contains("cart.html"), "Should navigate to the cart page."
