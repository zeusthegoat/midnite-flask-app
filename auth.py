from flask import request, jsonify
import os 

API_KEY = os.environ.get("API_KEY", "midniteisthecoolest")

def check_api_key():
    key = request.headers.get('x-api-key')
    if not key or key != API_KEY:
        response = jsonify({"message": "Unauthorised: Invalid or Missing Api Key"})
        response.status_code = 401
        return response
    return None