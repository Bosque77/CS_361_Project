import requests
import xml.etree.ElementTree as ET

def test_xml_to_json_conversion():
    url = "https://converter.api.terracette.com/Converter/xmltojson"
    headers = {
        'Content-Type': 'text/plain',
        'Accept': 'text/plain'
    }

    # Example XML data
    xml_data = """<root><name>John Doe</name><age>30</age></root>"""

    print(f"\nSending XML data:\n{xml_data}")

    try:
        response = requests.post(url, headers=headers, data=xml_data)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")

        # Attempt to parse the response as JSON
        try:
            json_response = response.json()
            print(f"Received JSON response:\n{json_response}")

            # Basic validation: check if expected keys are in the JSON response
            assert isinstance(json_response, dict), "Response is not a dictionary"
            assert "root" in json_response, "'root' key not found in JSON response"
            assert "name" in json_response["root"], "'name' key not found in 'root'"
            assert json_response["root"]["name"] == "John Doe", "Name does not match"
            assert "age" in json_response["root"], "'age' key not found in 'root'"
            assert json_response["root"]["age"] == "30", "Age does not match"

            print("XML to JSON conversion successful and validated!")

        except ValueError:
            print(f"Error: Response is not valid JSON. Raw response:\n{response.text}")
            assert False, "Response is not valid JSON"

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        assert False, f"Request failed: {e}"

if __name__ == "__main__":
    test_xml_to_json_conversion()
