import requests
import json

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

if __name__ == "__main__":
    print("Starting Ratings API Tests...")
    test_ratings_api()
    print("\nAll tests completed!")
