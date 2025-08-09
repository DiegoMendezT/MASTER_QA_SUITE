
# Lesson: Test Api P95 Smoke

Test: API Response Time (P95) Smoke Test
Selenium/API Features: [http_client, numpy for percentile]
AUT: JSONPlaceholder
Markers: @perf @api @external
Purpose: Verifies that the 95th percentile response time of a stable API
         endpoint is within an acceptable performance budget.

---

## Test Implementation

```python
"""
Test: API Response Time (P95) Smoke Test
Selenium/API Features: [http_client, numpy for percentile]
AUT: JSONPlaceholder
Markers: @perf @api @external
Purpose: Verifies that the 95th percentile response time of a stable API
         endpoint is within an acceptable performance budget.
"""
import pytest
import os
import time
import numpy as np
from utils.http_client import get_http_client

# --- Test Configuration ---
# Performance budget in milliseconds for API P95 response time.
API_P95_BUDGET_MS = int(os.environ.get("API_P95_MS", 500))
SAMPLE_COUNT = 10 # Number of API calls to make

@pytest.mark.perf
@pytest.mark.api
@pytest.mark.external
def test_api_p95_response_time_smoke(api_client):
    """
    Tests that a stable demo API endpoint's P95 response time is within budget.
    """
    # Arrange
    endpoint = "/posts/1"
    response_times_ms = []

    # Act: Call the endpoint multiple times and record response times
    print(f"Calling endpoint '{endpoint}' {SAMPLE_COUNT} times...")
    for i in range(SAMPLE_COUNT):
        start_time = time.perf_counter()
        try:
            response = api_client.get(endpoint)
            response.raise_for_status()  # Ensure the call was successful
        except Exception as e:
            pytest.fail(f"API call failed on attempt {i+1}: {e}")
        
        end_time = time.perf_counter()
        response_times_ms.append((end_time - start_time) * 1000)
        time.sleep(0.1) # Small delay between requests

    # Calculate the 95th percentile
    p95_response_time = np.percentile(response_times_ms, 95)

    # Assert
    print(f"P95 response time: {p95_response_time:.2f}ms (Budget: {API_P95_BUDGET_MS}ms)")
    
    assert p95_response_time <= API_P95_BUDGET_MS, \
        f"API P95 response time ({p95_response_time:.2f}ms) exceeded budget of {API_P95_BUDGET_MS}ms."

```

---

## Traceability

- **Test File**: `tests\perf\test_api_p95_smoke.py`
- **Markers**: ``@api`, `@external`, `@perf``
