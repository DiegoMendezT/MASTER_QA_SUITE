
# Lesson: Test Example

No description provided.

---

## Test Implementation

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.playwright
def test_example(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")

```

---

## Traceability

- **Test File**: `tests\playwright\test_example.py`
- **Markers**: ``@playwright``
