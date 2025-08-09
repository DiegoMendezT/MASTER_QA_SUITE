"""
Resilient HTTP Client using requests, requests-cache, and tenacity.

This module provides a singleton HTTP client configured with caching and
automatic retries for robustness and performance.

- Caching: Reduces redundant API calls for faster test execution and lower
  network load. Controlled by the `QA_FEATURE_CACHE_API_CALLS` feature flag.
- Retries: Handles transient network errors and flaky endpoints by automatically
  retrying failed requests with exponential backoff.
"""

import os
from functools import lru_cache

import requests
import requests_cache
import yaml
from requests.adapters import HTTPAdapter
from tenacity import retry, stop_after_attempt, wait_exponential

# Singleton instance of the HTTP client
_http_client = None

def get_config():
    """Loads configuration from settings.yaml, cached for performance."""
    # This is a simplified loader. In a real app, this might be part of a larger config service.
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@lru_cache(maxsize=1)
def get_http_client():
    """
    Returns a singleton instance of the configured HTTP client.

    The client is configured with retries and optional caching based on the
    project's settings.yaml file.

    Returns:
        requests.Session: The configured session object.
    """
    global _http_client
    if _http_client is not None:
        return _http_client

    config = get_config()
    use_cache = config.get('feature_flags', {}).get('QA_FEATURE_CACHE_API_CALLS', False)

    if use_cache:
        # Install cache with a backend (e.g., SQLite)
        # This will create a `http_cache.sqlite` file in the current directory
        # match_headers=True ensures that requests with different headers are cached separately.
        requests_cache.install_cache(
            'http_cache', 
            backend='sqlite', 
            expire_after=3600, 
            match_headers=True
        )

    session = requests.Session()

    # Configure retry mechanism
    retry_strategy = retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )

    # Apply the retry strategy to all HTTP methods
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Set common headers
    session.headers.update({
        'User-Agent': 'MASTER-QA-SUITE/2.0',
        'Accept': 'application/json, */*',
    })

    _http_client = session
    return _http_client

# Example of how to use the client:
# from utils.http_client import get_http_client
#
# client = get_http_client()
# try:
#     response = client.get('https://httpbin.org/get')
#     response.raise_for_status()
#     print(response.json())
# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")
