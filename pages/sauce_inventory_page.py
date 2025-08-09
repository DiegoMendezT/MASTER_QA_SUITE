"""
Page Object for the Sauce Demo Inventory Page.

This class represents the main product inventory page that appears after a
successful login. It encapsulates the elements and actions available on this page.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SauceInventoryPage(BasePage):
    """
    Represents the product inventory page and its interactions.
    """
    # --- Locators ---
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    
    def __init__(self, driver, config):
        """
        Initializes the SauceInventoryPage.
        """
        super().__init__(driver, config)

    def get_title(self):
        """
        Gets the title of the inventory page.
        
        Returns:
            The page title text as a string.
        """
        return self.get_element_text(self.PAGE_TITLE)

    def is_cart_displayed(self):
        """
        Checks if the shopping cart icon is visible.
        
        Returns:
            True if the cart is displayed, False otherwise.
        """
        return self.find_element(self.SHOPPING_CART_ICON).is_displayed()

    def get_inventory_item_count(self):
        """
        Counts the number of inventory items on the page.
        
        Returns:
            The number of inventory items.
        """
        return len(self.find_elements(self.INVENTORY_ITEMS))

    def add_to_cart_by_name(self, item_name):
        """
        Adds a specific item to the cart by its name using its data-test attribute.

        Args:
            item_name (str): The name of the item to add.
        """
        # Convert item name to the format used in data-test attributes
        # e.g., "Sauce Labs Backpack" -> "add-to-cart-sauce-labs-backpack"
        data_test_name = "add-to-cart-" + item_name.lower().replace(" ", "-")
        
        add_to_cart_button_locator = (
            By.CSS_SELECTOR,
            f"button[data-test='{data_test_name}']"
        )
        self.click(add_to_cart_button_locator)
