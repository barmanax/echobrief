import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_KEY")
if not API_KEY:
    raise ValueError("ERROR: Could not find 'GEMINI_KEY' in environment variables or .env file.")

# --- SANITIZED: replace internal gateway with a placeholder ---
HOST = "https://<YOUR_API_GATEWAY_HOST>/app-gateway"
ENDPOINT = "/api/v2/chat"
API_URL = HOST + ENDPOINT

# --- SANITIZED: keep header shape but avoid internal naming if proprietary ---
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}


def call_custom_gemini_api(prompt: str, user_id: str = "<YOUR_USER_ID>") -> str:
    body = {
        "userId": user_id,
        "model": "VertexGemini",
        "prompt": prompt,
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=body)
        response.raise_for_status()

        response_data = response.json()
        model_response_text = response_data.get("msg")

        if model_response_text:
            return model_response_text.strip()
        else:
            print("ERROR: 'msg' field not found in API response.")
            print("Full response:", json.dumps(response_data, indent=2))
            return "Error: Could not parse a valid response from the API."

    except Exception as e:
        print(f"An unexpected error occurred in the API call: {e}")
        raise


def extract_events_with_gemini(transcript: str) -> str:
    """
    Takes a transcript and returns a JSON string of structured events by
    calling the custom API and instructing the AI to normalize location names.
    """
    prompt = f"""
Analyze the following emergency radio transcript. Your task is to extract key events and structure them as a JSON list.

Here is a strict list of valid location IDs for the apartment map:
- "entrance"
- "bathroom"
- "dining-room"
- "bedroom-1"
- "tv-room"
- "bedroom-2"
- "living-room"
- "bedroom-3"

When you identify a location in the transcript, you MUST map it to one of the exact IDs from the list above. For example:
- If the transcript says "the first bedroom", "bedroom one", or "the bedroom on the top right", the location value MUST BE "bedroom-1".
- If the transcript says "the TV area" or "television room", the location value MUST BE "tv-room".
- If the transcript says "the front door", the location value MUST BE "entrance".

Each extracted event in the JSON list must include:
- "time_raw": The timestamp from the transcript (e.g., "01:58").
- "location": One of the exact, predefined location IDs from the list above.
- "event_summary": A brief, clear summary of what happened.
- "entities": A list of units or personnel involved (e.g., ["Unit 714", "Dispatch"]).
- "urgency": A rating of "high", "medium", or "low".

Transcript:
---
{transcript}
---

Return ONLY the raw JSON list, with no other text, comments, or markdown formatting.
"""

    print("Requesting structured event extraction with location normalization from model...")
    json_string = call_custom_gemini_api(prompt)
    print("Structured events received.")
    return json_string.strip().replace("```json", "").replace("```", "")


def generate_summary_with_gemini(transcript: str) -> str:
    """
    Takes a transcript and returns a narrative summary paragraph.
    """
    prompt = f"""
Summarize the following emergency radio transcript into a concise, professional paragraph suitable for an after-action report.
Focus on the sequence of events, key discoveries, and the final outcome.

Transcript:
---
{transcript}
---

Return ONLY the summary paragraph, with no other text or titles.
"""

    print("Requesting narrative summary from model...")
    summary_text = call_custom_gemini_api(prompt)
    print("Narrative summary received.")
    return summary_text.strip()
