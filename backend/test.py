import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
API_URL = "https://example-llm-gateway.com/api/v1/chat"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "userId": "test-user",
    "model": "generic-llm",
    "prompt": "What color is the sky on a clear day?",
}

response = requests.post(API_URL, headers=HEADERS, json=payload)
response.raise_for_status()

print(response.json())
