import requests
import json
import pytest

def test_ratings_api():
    # API endpoint
    url = "https://cs-361-project-three.vercel.app/api/average"
    
    # Test cases
    test_cases = [
        {
            "name": "Valid ratings",
            "data": {"ratings": [4, 5, 3, 5]},
            "expected_status": 200,
            "expected_key": "average"
        },
        {
            "name": "Empty array",
            "data": {"ratings": []},
            "expected_status": 200,
            "expected_key": "error"
        },
        {
            "name": "Invalid input (string)",
            "data": {"ratings": ["not", "a", "number"]},
            "expected_status": 400,
            "expected_key": "error"
        },
        {
            "name": "Single number",
            "data": {"ratings": [42]},
            "expected_status": 200,
            "expected_key": "average"
        },
        {
            "name": "Decimal numbers",
            "data": {"ratings": [1.5, 2.5, 3.5, 4.5]},
            "expected_status": 200,
            "expected_key": "average"
        }
    ]
    
    # Run test cases
    for test in test_cases:
        print(f"\n{'='*50}")
        print(f"Test: {test['name']}")
        print(f"Request: POST {url}")
        print(f"Payload: {json.dumps(test['data'], indent=2)}")
        
        try:
            # Make the request
            response = requests.post(
                url,
                json=test['data'],
                headers={"Content-Type": "application/json"}
            )
            
            # Print response
            print(f"Status Code: {response.status_code}")
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            
            # Validate response
            if response.status_code == test['expected_status']:
                if test['expected_key'] in response.json():
                    print("✅ Test passed!")
                else:
                    print(f"❌ Test failed: Expected key '{test['expected_key']}' not found in response")
            else:
                print(f"❌ Test failed: Expected status {test['expected_status']}, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error making request: {str(e)}")

def test_cors_headers():
    """Test that CORS headers are properly set in the API responses."""
    url = "https://cs-361-project-three.vercel.app/api/average"
    
    # Test OPTIONS request
    print("\n" + "="*50)
    print("Testing CORS headers with OPTIONS request")
    response = requests.options(url)
    
    # Debug: Print all response headers
    print("\nResponse Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    
    # Check status code
    assert response.status_code == 204, f"Expected status 204, got {response.status_code}"
    
    # Check CORS headers (case-insensitive check)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert 'access-control-allow-origin' in headers_lower, \
        f"Missing CORS header: Access-Control-Allow-Origin. Headers present: {list(response.headers.keys())}"
    assert headers_lower['access-control-allow-origin'] == '*', \
        f"Incorrect CORS origin. Got: {headers_lower.get('access-control-allow-origin')}"
    
    # Test POST request
    print("\n" + "="*50)
    print("Testing CORS headers with POST request")
    response = requests.post(
        url,
        json={"ratings": [1, 2, 3, 4, 5]},
        headers={"Content-Type": "application/json"}
    )
    
    # Debug: Print all response headers
    print("\nResponse Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")
    
    # Check status code
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Check CORS headers (case-insensitive check)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    assert 'access-control-allow-origin' in headers_lower, \
        f"Missing CORS header: Access-Control-Allow-Origin. Headers present: {list(response.headers.keys())}"
    assert headers_lower['access-control-allow-origin'] == '*', \
        f"Incorrect CORS origin. Got: {headers_lower.get('access-control-allow-origin')}"
    
    print("CORS headers test passed!")

if __name__ == "__main__":
    print("Starting Ratings API Tests...")
    test_ratings_api()
    test_cors_headers()
    print("\nAll tests completed!")
