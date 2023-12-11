import requests
import json

# OpenFaas function URL
OPENFAAS_URL = "http://localhost:8080/function/eduscan-handler"
# Test input
TEST_INPUT = {"event": {"Records": [{"s3": {"object": {"key": "test_0.mp4"}}}]}, "context": {}}

def parse_response(response_text):
    start_token = "=== Begin Response ==="
    end_token = "=== End Response ==="
    
    # Split the response_text by start_token and take the second part
    # Then split that part by end_token and take the first part
    result = response_text.split(start_token, 1)[-1].split(end_token, 1)[0]
    
    # Strip leading and trailing whitespace
    result = result.strip()
    
    return result

# Convert the test input to JSON
data = json.dumps(TEST_INPUT)
# Invoke the function
response = requests.post(OPENFAAS_URL, data=data)
# Parse the response text
response_text = parse_response(response.text)
# Print the response text
print(response_text)