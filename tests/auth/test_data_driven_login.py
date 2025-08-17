"""
Test: Data-Driven Login

Selenium/API Features: [Data-Driven Testing, JSON, Allure]
AUT: Sauce Demo
Markers: @integration @auth
Purpose: This test verifies the login functionality with multiple user profiles
         by reading test data from an external JSON file.
"""
import json
import os

import allure
import pytest

from pages.sauce_login_page import SauceLoginPage


def load_user_data():
    """Loads user data from the users.json file."""
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')
    with open(data_path, 'r') as f:
        return json.load(f)

@pytest.mark.integration
@pytest.mark.auth
@allure.feature("Authentication")
@allure.story("Data-Driven Login Scenarios")
class TestDataDrivenLogin:

    @pytest.mark.parametrize("user_data", load_user_data())
    def test_login_with_different_users(self, driver, config, user_data):
        """
        Tests login with various user credentials from a data file.
        """
        username = user_data['user']
        password = user_data['pass']
        should_pass = user_data['expected_to_pass']

        allure.dynamic.title(f"Test Login: {username}")
        allure.dynamic.parameter("user", username)
        allure.dynamic.parameter("expected_to_pass", should_pass)

        with allure.step(f"Attempting login for user: {username}"):
            login_page = SauceLoginPage(driver, config)
            login_page.load()
            login_page.login(username, password)

        with allure.step("Verifying login outcome"):
            if should_pass:
                assert "inventory.html" in driver.current_url, f"User '{username}' was expected to log in but failed."
                allure.attach(f"Login successful for {username} as expected.", name="Login Status")
            else:
                assert "inventory.html" not in driver.current_url, f"User '{username}' was expected to fail login but succeeded."
                error_message = login_page.get_error_message()
                assert error_message, "Error message should be displayed for failed login."
                allure.attach(f"Login failed for {username} as expected. Error: {error_message}", name="Login Status")
