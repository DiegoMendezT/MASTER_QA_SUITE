
# Lesson: Test Cart Consistency

Test: UI to API Cart Consistency (Simulated)

Selenium/API Features: [POM, execute_script, localStorage, Custom API Client]
AUT: Sauce Demo
Markers: @integration
Purpose: This test verifies that adding an item to the cart in the UI is
         correctly reflected in the backend state, as retrieved from a
         simulated API. It ensures data consistency between the front-end
         action and the backend's view of the cart.

---

## Test Implementation

```python
"""
Test: UI to API Cart Consistency (Simulated)

Selenium/API Features: [POM, execute_script, localStorage, Custom API Client]
AUT: Sauce Demo
Markers: @integration
Purpose: This test verifies that adding an item to the cart in the UI is
         correctly reflected in the backend state, as retrieved from a
         simulated API. It ensures data consistency between the front-end
         action and the backend's view of the cart.
"""
import json

import allure
import pytest

from pages.sauce_inventory_page import SauceInventoryPage
from pages.sauce_login_page import SauceLoginPage
from utils.api_client import get_api_client


@pytest.mark.integration
@allure.feature("Cart Management")
@allure.story("Verify cart consistency between UI and API")
@allure.title("Test Cart Consistency After Adding Item")
@allure.description("""
    This test verifies that adding an item to the cart via the UI is
    correctly reflected in the backend state, simulated via an API.
    It ensures data consistency between the frontend action and the backend's view.
""")
def test_cart_consistency_after_adding_item(logged_in_driver, config):
    """
    Tests that localStorage cart after UI action matches simulated API cart data.
    Uses the 'logged_in_driver' fixture to start on the inventory page.
    """
    # Arrange: Initialize pages and API client
    driver = logged_in_driver  # Use the already logged-in driver
    inventory_page = SauceInventoryPage(driver, config)
    api_client = get_api_client(config) # Simplified API client retrieval

    # UI Action: Add an item to the cart
    item_to_add = 'Sauce Labs Backpack'
    with allure.step(f"Add '{item_to_add}' to cart via UI"):
        inventory_page.add_to_cart_by_name(item_to_add)
        print(f"UI: Added '{item_to_add}' to cart.")

    # Act: Retrieve cart state from both UI (localStorage) and a simulated API
    with allure.step("Retrieve cart state from UI and API"):
        # 1. Get cart from the browser's localStorage and parse it
        ui_cart_json = driver.execute_script("return window.localStorage.getItem('cart-contents');")
        ui_cart_list = json.loads(ui_cart_json) if ui_cart_json else []
        allure.attach(json.dumps(ui_cart_list, indent=2), name="UI Cart (localStorage)", attachment_type=allure.attachment_type.JSON)
        print(f"UI localStorage 'cart-contents': {ui_cart_list}")
        
        # 2. Get cart data from the (simulated) API
        api_cart = api_client.get_cart(session_token='dummy-auth-token-for-standard-user')
        api_cart_items = api_cart.get('items', [])
        allure.attach(json.dumps(api_cart_items, indent=2), name="API Cart (simulated)", attachment_type=allure.attachment_type.JSON)
        print(f"Simulated API response for cart: {api_cart_items}")

    # Assert: Verify that the cart contents are consistent
    with allure.step("Verify cart consistency"):
        assert ui_cart_list, "Cart contents should not be empty in UI localStorage"
        assert api_cart_items, "Cart items should not be empty in API response"
        
        assert len(ui_cart_list) == len(api_cart_items), \
            f"Cart inconsistency! UI shows {len(ui_cart_list)} item(s), but API reports {len(api_cart_items)}."

        print(f"SUCCESS: UI cart count ({len(ui_cart_list)}) matches API cart count ({len(api_cart_items)}).")

```

---

## Traceability

- **Test File**: `tests\integration\test_cart_consistency.py`
- **Markers**: ``@integration``
