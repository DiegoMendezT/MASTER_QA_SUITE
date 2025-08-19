
# Lesson: Test Axe Home And Cart

Test: Accessibility Smoke Tests using axe-core
Selenium/API Features: [Custom axe-core injection, execute_async_script, POM]
AUT: Sauce Demo
Markers: @a11y @ui
Purpose: Verifies that key pages of the application do not have serious or
         critical accessibility violations, ensuring a baseline of usability.

---

## Test Implementation

```python
"""
Test: Accessibility Smoke Tests using axe-core
Selenium/API Features: [Custom axe-core injection, execute_async_script, POM]
AUT: Sauce Demo
Markers: @a11y @ui
Purpose: Verifies that key pages of the application do not have serious or
         critical accessibility violations, ensuring a baseline of usability.
"""
import os

import pytest

from pages.sauce_inventory_page import SauceInventoryPage
from pages.sauce_login_page import SauceLoginPage
from utils.a11y import inject_axe, run_axe

# --- Test Configuration ---
# Maximum number of serious or critical violations allowed before failing.
# Can be overridden by an environment variable.
A11Y_MAX_SERIOUS_VIOLATIONS = int(os.environ.get("A11Y_MAX_SERIOUS", 0))

def analyze_violations(violations: list) -> tuple[int, list]:
    """
    Analyzes a list of axe violations and filters for serious or critical issues.
    
    Args:
        violations: A list of violation dictionaries from axe-core.

    Returns:
        A tuple containing the count of serious/critical violations and the
        formatted details of those violations.
    """
    serious_violations = []
    for v in violations:
        if v['impact'] in ['serious', 'critical']:
            # Format a readable message for each serious violation
            nodes_summary = ", ".join([node['html'] for node in v['nodes'][:3]]) # Show first 3 nodes
            msg = (
                f"  - ID: {v['id']} ({v['impact']})\n"
                f"    Help: {v['helpUrl']}\n"
                f"    Description: {v['description']}\n"
                f"    Nodes: {nodes_summary}"
            )
            serious_violations.append(msg)
            
    return len(serious_violations), serious_violations

@pytest.mark.a11y
@pytest.mark.ui
def test_accessibility_on_inventory_and_cart_pages(driver, config):
    """
    Performs accessibility scan on the inventory and cart pages after login.
    """
    # --- Arrange ---
    # Log in to the application
    user = config['users']['sauce_standard_user']
    login_page = SauceLoginPage(driver, config)
    login_page.load()
    login_page.login(user['username'], user['password'])
    
    # Inject the axe-core script into the page
    inject_axe(driver)

    # --- Act & Assert on Inventory Page ---
    inventory_page = SauceInventoryPage(driver, config)
    assert inventory_page.is_cart_displayed(), "Failed to load inventory page after login."
    
    print("\nRunning axe-core on Inventory Page...")
    inventory_violations = run_axe(driver)
    
    serious_count, serious_details = analyze_violations(inventory_violations)
    
    assert serious_count <= A11Y_MAX_SERIOUS_VIOLATIONS, \
        f"Inventory Page: Found {serious_count} serious/critical accessibility violations.\n" + \
        "\n".join(serious_details)
    
    print(f"Inventory Page: Found {serious_count} serious/critical violations. (Threshold: {A11Y_MAX_SERIOUS_VIOLATIONS})")

    # --- Act & Assert on Cart Page ---
    # Navigate to the cart page
    inventory_page.click(inventory_page.SHOPPING_CART_ICON)
    
    print("\nRunning axe-core on Cart Page...")
    cart_violations = run_axe(driver)
    
    serious_count, serious_details = analyze_violations(cart_violations)
    
    assert serious_count <= A11Y_MAX_SERIOUS_VIOLATIONS, \
        f"Cart Page: Found {serious_count} serious/critical accessibility violations.\n" + \
        "\n".join(serious_details)

    print(f"Cart Page: Found {serious_count} serious/critical violations. (Threshold: {A11Y_MAX_SERIOUS_VIOLATIONS})")

```

---

## Traceability

- **Test File**: `tests\a11y\test_axe_home_and_cart.py`
- **Markers**: ``@a11y`, `@ui``
