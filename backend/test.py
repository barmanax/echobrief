# backend/test.py

import os
import requests
import json
from dotenv import load_dotenv

# --- 1. SETUP AND CONFIGURATION ---
load_dotenv()

api_key = os.getenv("GEMINI_KEY")

if not api_key:
    print("❌ ERROR: Could not find 'GEMINI_KEY' in environment variables.")
    print("   Please create a .env file in the backend folder with GEMINI_KEY='your_key_here'")
    exit()

# --- SANITIZED: internal gateway removed ---
host = "https://<YOUR_API_GATEWAY_HOST>/app-gateway"
endpoint = "/api/v2/chat"
api_url = host + endpoint

# --- SANITIZED: header name made generic ---
HEADERS = {
    "x-api-key": api_key,
    "Content-Type": "application/json",
}

BODY = {
    "userId": "<YOUR_USER_ID>",
    "model": "VertexGemini",
    "prompt": "In one sentence, what is the color of the sky on a clear day?",
    "system": "You are a helpful assistant.",
}

# --- 3. MAKE THE API CALL ---
print("Attempting to call custom Gemini endpoint...")

try:
    response = requests.post(api_url, headers=HEADERS, json=BODY)
    response.raise_for_status()

    response_data = response.json()

    # According to the output, the actual text is in the 'msg' field.
    model_response_text = response_data.get("msg")

    if model_response_text:
        print("\n--- ✅ TEST SUCCESSFUL ---")
        print("✅ API call succeeded! Your key and endpoint are working.")
        print("\nModel's Response:")
        print(f"{model_response_text.strip()}")
    else:
        print("\n--- ❌ TEST FAILED (but request was successful) ---")
        print("❌ Could not find the 'msg' field in the response.")
        print("\nFull Response:")
        print(json.dumps(response_data, indent=2))

except requests.exceptions.HTTPError as http_err:
    print("\n--- ❌ TEST FAILED ---")
    print(f"❌ HTTP Error occurred: {http_err}")
    print(f"   Status Code: {http_err.response.status_code}")
    print(f"   Response Body: {http_err.response.text}")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
