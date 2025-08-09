
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
import pytest
import json
from pages.sauce_login_page import SauceLoginPage
from pages.sauce_inventory_page import SauceInventoryPage
from utils.api_client import get_api_client

@pytest.mark.integration
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
    inventory_page.add_to_cart_by_name(item_to_add)
    print(f"UI: Added '{item_to_add}' to cart.")

    # Act: Retrieve cart state from both UI (localStorage) and a simulated API
    
    # 1. Get cart from the browser's localStorage and parse it
    ui_cart_json = driver.execute_script("return window.localStorage.getItem('cart-contents');")
    ui_cart_list = json.loads(ui_cart_json) if ui_cart_json else []
    print(f"UI localStorage 'cart-contents': {ui_cart_list}")
    
    # 2. Get cart data from the (simulated) API
    # In a real scenario, we'd use an auth token from the UI session
    api_cart = api_client.get_cart(session_token='dummy-auth-token-for-standard-user')
    api_cart_items = api_cart.get('items', [])
    print(f"Simulated API response for cart: {api_cart_items}")

    # Assert: Verify that the cart contents are consistent
    assert ui_cart_list, "Cart contents should not be empty in UI localStorage"
    assert api_cart_items, "Cart items should not be empty in API response"
    
    # For this test, we'll just check the number of items.
    # A more complex test could compare the exact product IDs.
    assert len(ui_cart_list) == len(api_cart_items), \
        f"Cart inconsistency! UI shows {len(ui_cart_list)} item(s), but API reports {len(api_cart_items)}."

    # The UI stores item IDs (e.g., 4), while our simulated API might use names or different IDs.
    # This is a realistic integration challenge. For now, we'll rely on the count.
    # A more robust solution would be to map UI IDs to API product IDs.
    print(f"SUCCESS: UI cart count ({len(ui_cart_list)}) matches API cart count ({len(api_cart_items)}).")

```

---

## Traceability

- **Test File**: `tests\integration\test_cart_consistency.py`
- **Markers**: ``@integration``
