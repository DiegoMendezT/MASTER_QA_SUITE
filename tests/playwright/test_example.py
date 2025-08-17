import pytest
from playwright.sync_api import Page, expect


# --- Temporarily disabled for CI isolation ---
# @pytest.mark.playwright
# def test_example(page: Page):
#     page.goto("https://playwright.dev/")
#     expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
