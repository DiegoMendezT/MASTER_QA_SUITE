
# Lesson: Test 01 Get Post Schema

Test: API Schema Validation
Selenium/API Features: [requests, jsonschema]
AUT: JSONPlaceholder API
Markers: @api @external
Purpose: To verify that the API response for a single post conforms to the expected JSON schema. This ensures the API contract is being met.

---

## Test Implementation

```python
"""
Test: API Schema Validation
Selenium/API Features: [requests, jsonschema]
AUT: JSONPlaceholder API
Markers: @api @external
Purpose: To verify that the API response for a single post conforms to the expected JSON schema. This ensures the API contract is being met.
"""
import json
import os

import pytest
from jsonschema import validate

from utils.http_client import get_http_client


def load_schema(file_name):
    """Loads a JSON schema from the contracts directory."""
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'contracts', file_name)
    with open(path, 'r') as f:
        return json.load(f)

@pytest.mark.api
@pytest.mark.external
def test_01_get_post_schema(api_client, config):
    """
    Tests that a single post from JSONPlaceholder API matches the defined schema.
    """
    # Arrange
    post_id = 1
    url = f"{config['apis']['jsonplaceholder']}/posts/{post_id}"
    post_schema = load_schema('post.schema.json')
    
    # Act
    response = api_client.get(url)
    response.raise_for_status()  # Ensure the request was successful
    response_json = response.json()
    
    # Assert
    # Validate the response against the schema
    validate(instance=response_json, schema=post_schema)
    
    # Optional: A few direct assertions for key fields
    assert response_json['id'] == post_id
    assert response_json['userId'] is not None

```

---

## Traceability

- **Test File**: `tests\api\test_01_get_post_schema.py`
- **Markers**: ``@api`, `@external``
