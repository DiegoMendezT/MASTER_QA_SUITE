"""
Page Object for the User Profile (Inventory) Page.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProfilePage(BasePage):
    """
    Represents the user's main view after logging in, which is the inventory page.
    """

    # --- Locators ---
    _inventory_container = (By.ID, "inventory_container")
    _shopping_cart_link = (By.CLASS_NAME, "shopping_cart_link")
    _sort_container = (By.CLASS_NAME, "product_sort_container")
    _page_title = (By.CLASS_NAME, "title")

    def __init__(self, driver, config):
        """
        Initializes the ProfilePage.
        """
        super().__init__(driver, config)

    def is_inventory_displayed(self):
        """
        Checks if the main inventory container is visible.
        
        Returns:
            bool: True if the inventory is visible, False otherwise.
        """
        return self.is_element_visible(self._inventory_container)

    def get_page_title(self):
        """
        Gets the title displayed on the page (e.g., "Products").
        
        Returns:
            str: The text of the page title.
        """
        return self.get_element_text(self._page_title)

    def get_active_sort_option(self):
        """
        Gets the text of the currently active sort option.
        
        Returns:
            str: The text of the active sort option.
        """
        return self.get_element_text(self._sort_container)

    def click_shopping_cart(self):
        """
        Clicks the shopping cart icon to navigate to the cart page.
        """
        self.click(self._shopping_cart_link)
