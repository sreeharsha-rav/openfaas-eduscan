import sys
import json
from face_recognition_module import face_recognition_handler

def handle(req):
    try:
        # parse the JSON request body
        request = json.loads(req)
        event = request["event"]
        context = request["context"]

        # invoke the handler function
        result = face_recognition_handler(event, context)

        # return response
        return result

    except Exception as e:
        # return error message
        return {
			'statusCode': 500,
			'body': f"Error processing handle request: {str(e)}"
		}

if __name__ == "__main__":
    # invoke handle function
    response = handle(sys.stdin.read())

    # log response to stdout
    print("=== Begin Response ===")
    print(response)
    print("=== End Response ===")