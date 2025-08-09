# Example Tests

## Playwright: Smoke Login (Sauce Demo)
```python
def test_example(page):
    page.goto("https://www.saucedemo.com/")
    assert "Swag Labs" in page.title()
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_selector("data-test=inventory-container")
    assert "inventory" in page.url
```
