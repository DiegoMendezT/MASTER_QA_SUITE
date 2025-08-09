"""
API Client for MASTER QA SUITE

This module provides a centralized client for making API calls.
It can be configured to work in 'simulated' or 'live' mode.
"""
import requests
from tenacity import retry, stop_after_attempt, wait_fixed


class ApiClient:
    """A client for interacting with the application's API."""

    def __init__(self, mode='simulated', base_url=None):
        """
        Initializes the API client.

        Args:
            mode (str): The mode of operation, 'simulated' or 'live'.
            base_url (str, optional): The base URL for live API endpoints.
        """
        self.mode = mode
        self.base_url = base_url
        self.session = requests.Session()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def get_session(self, user_id):
        """
        Retrieves session data for a given user.

        In 'simulated' mode, returns a dummy dictionary.
        In 'live' mode, would make a real API call.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: The user's session data.
        """
        if self.mode == 'simulated':
            print(f"SIMULATED: Fetching session for user_id: {user_id}")
            return {
                'userId': user_id,
                'username': 'standard_user',
                'token': 'dummy-auth-token-for-standard-user',
                'expires': '2025-12-31T23:59:59Z'
            }
        
        # Live mode implementation would go here
        if not self.base_url:
            raise ValueError("Base URL must be set for live mode.")
        
        response = self.session.get(f"{self.base_url}/api/v1/session/{user_id}")
        response.raise_for_status()
        return response.json()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def get_cart(self, session_token):
        """
        Retrieves cart data using a session token.

        In 'simulated' mode, returns a dummy dictionary.
        In 'live' mode, would make a real API call.

        Args:
            session_token (str): The authentication token for the session.

        Returns:
            dict: The user's cart data.
        """
        if self.mode == 'simulated':
            print(f"SIMULATED: Fetching cart for token: {session_token[:10]}...")
            # This dummy data simulates a cart with one item
            return {
                'cartId': 'cart-dummy-123',
                'items': [
                    {'productId': 'sauce-labs-backpack', 'quantity': 1}
                ],
                'itemCount': 1
            }

        # Live mode implementation would go here
        if not self.base_url:
            raise ValueError("Base URL must be set for live mode.")
            
        headers = {'Authorization': f'Bearer {session_token}'}
        response = self.session.get(f"{self.base_url}/api/v1/cart", headers=headers)
        response.raise_for_status()
        return response.json()

# Global factory function to be used by fixtures
def get_api_client(config, mode=None):
    """
    Factory function to get an instance of the ApiClient.
    
    Args:
        config (dict): The main application configuration.
        mode (str, optional): The integration mode ('simulated' or 'live'). 
                              If not provided, it's inferred from config.

    Returns:
        ApiClient: An instance of the ApiClient.
    """
    # If mode is not explicitly passed, try to get it from the integration config part
    if mode is None:
        mode = config.get('integration', {}).get('mode', 'simulated')

    base_url = config.get('urls', {}).get('sauce_demo_api')
    return ApiClient(mode=mode, base_url=base_url)
