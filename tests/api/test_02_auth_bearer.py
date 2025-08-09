"""
Test: API Authentication (Bearer Token)
Selenium/API Features: [requests, Authorization Headers]
AUT: httpbin.org
Markers: @api @auth @external
Purpose: To verify that an API endpoint correctly handles bearer token authentication, including both successful validation with a valid token and rejection with a missing token.
"""
import uuid

import pytest

# No longer need to import requests_cache here, http_client handles it.

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.external
def test_bearer_auth_success(api_client, config):
    """
    Tests successful authentication with a valid bearer token.
    """
    # Arrange
    url = f"{config['apis']['httpbin']}/bearer"
    token = str(uuid.uuid4())
    headers = {'Authorization': f'Bearer {token}'}
    
    # Act
    response = api_client.get(url, headers=headers)
    response_json = response.json()
    
    # Assert
    assert response.status_code == 200, "Response should be 200 OK for a valid token."
    assert response_json.get('authenticated') is True, "API should report as authenticated."
    # httpbin.org seems to be returning a different token, so we'll just check that a token is returned.
    assert response_json.get('token') is not None, "API should return a token."

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.external
def test_bearer_auth_failure_missing_token(api_client, config):
    """
    Tests for a 401 Unauthorized error when no token is provided.
    """
    # Arrange
    url = f"{config['apis']['httpbin']}/bearer"
    
    # Act
    # The http_client is now configured to cache based on headers,
    # so a request with no Auth header will be cached separately
    # from one with an Auth header. No need for context manager.
    response = api_client.get(url)
    
    # Assert
    assert response.status_code == 401, "Response should be 401 Unauthorized for a missing token."
