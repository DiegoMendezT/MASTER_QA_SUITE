"""
Test: UI to API Session Consistency (Simulated)

Selenium/API Features: [POM, execute_script, localStorage, Custom API Client]
AUT: Sauce Demo
Markers: @integration
Purpose: This test verifies that the user session created in the UI is consistent
         with the session data retrieved from a simulated API backend. It ensures
         that the front-end state (like localStorage) matches the backend's view.
"""
import pytest

from pages.sauce_login_page import SauceLoginPage
from utils.api_client import get_api_client


@pytest.mark.integration
def test_session_consistency_after_login(logged_in_driver, active_integration_config, config):
    """
    Tests that the browser cookie after UI login matches simulated API session data.
    Uses the 'logged_in_driver' fixture to simplify the test setup.
    """
    # Arrange: The logged_in_driver fixture has already handled the login.
    driver = logged_in_driver
    api_client = get_api_client(config) # Simplified API client retrieval
    
    # Expected username from the active integration configuration
    expected_username = active_integration_config['user']

    # Act: Retrieve session state from both the UI (cookie) and the simulated API
    
    # 1. Get session username from the browser's cookie
    ui_username_cookie = driver.get_cookie('session-username')
    ui_username = ui_username_cookie['value'] if ui_username_cookie else None
    print(f"UI cookie 'session-username': {ui_username}")
    
    # 2. Get session data from the (simulated) API
    # In a real scenario, we might use a user ID from the UI to query the API
    api_session = api_client.get_session(user_id=expected_username)
    api_username = api_session.get('username')
    print(f"Simulated API response for session: {api_session}")

    # Assert: Verify that the session is consistent and matches the expected user
    assert ui_username is not None, "Username cookie should be present after login"
    assert api_username is not None, "Username should be returned from the API"
    
    assert ui_username == expected_username, \
        f"UI session user '{ui_username}' does not match expected user '{expected_username}'."
        
    assert api_username == expected_username, \
        f"API session user '{api_username}' does not match expected user '{expected_username}'."

    assert ui_username == api_username, \
        f"Session inconsistency! UI user '{ui_username}' does not match API user '{api_username}'."

    print(f"SUCCESS: UI username '{ui_username}' matches API username '{api_username}'.")
