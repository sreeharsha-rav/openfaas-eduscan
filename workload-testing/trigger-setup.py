import boto3
import requests
import json
import time
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

# OpenFaas function URL
OPENFAAS_URL = "http://localhost:8080/function/eduscan-handler"

# Function to convert the test input to JSON
def convert_to_input_format(key):
    # Create a dictionary with the required structure
    data = {
        "event": {
            "Records": [
                {
                    "s3": {
                        "object": {
                            "key": key
                        }
                    }
                }
            ]
        },
        "context": {}
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)
    return json_data

# Function to parse the response text
def parse_response(response_text):
    start_token = "=== Begin Response ==="
    end_token = "=== End Response ==="
    # Split the response_text by start_token and take the second part
    # Then split that part by end_token and take the first part
    result = response_text.split(start_token, 1)[-1].split(end_token, 1)[0]
    # Strip leading and trailing whitespace
    result = result.strip()
    return result

# Function to listen to the S3 bucket and invoke the OpenFaas function
def main():
    # Create an S3 client
    s3 = boto3.client(
        's3',
        region_name = AWS_REGION,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    # The name of your S3 bucket
    bucket_name = 'eduscan-lambda-input'

    # Get the initial key count and keys
    initial_response = s3.list_objects_v2(Bucket=bucket_name)
    initial_key_count = initial_response['KeyCount']
    print("Initial key count: " + str(initial_key_count))
    initial_keys = []   # List of initial keys
    if initial_key_count > 0:
        initial_keys = [item['Key'] for item in initial_response['Contents']]
    print("Initial keys: " + str(initial_keys))

    # Continuously poll the bucket for new keys
    while True:
        response = s3.list_objects_v2(Bucket=bucket_name)
        key_count = response['KeyCount']
        print("Current key count: " + str(key_count))
        if key_count > 0:
            # Get the new keys
            keys = [item['Key'] for item in response['Contents']]
            new_keys = list(set(keys) - set(initial_keys))
            # Invoke the function for each new key
            for key in new_keys:
                # Convert to input format
                data = convert_to_input_format(key)
                # Invoke the function
                response = requests.post(OPENFAAS_URL, data=data)
                # Parse the response text
                response_text = parse_response(response.text)
                # Print the response text
                print(response_text)
            # Update the initial keys and key count
            initial_key_count = key_count
            initial_keys = keys
        # Wait for 0.1s
        time.sleep(0.1)

if __name__ == "__main__":
    main()