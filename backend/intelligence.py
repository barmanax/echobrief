import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
if not API_KEY:
    raise ValueError("Missing LLM_API_KEY")

API_URL = "https://example-llm-gateway.com/api/v1/chat"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def call_custom_llm_api(prompt: str, user_id: str = "anonymous") -> str:
    payload = {
        "userId": user_id,
        "model": "generic-llm",
        "prompt": prompt,
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()
    if "msg" not in data:
        raise ValueError("Invalid LLM response format")

    return data["msg"].strip()


def extract_events_with_llm(transcript: str) -> str:
    prompt = f"""
    Analyze the following emergency radio transcript and extract key events.
    Return ONLY a raw JSON list.

    Valid location IDs:
    - entrance
    - bathroom
    - dining-room
    - bedroom-1
    - tv-room
    - bedroom-2
    - living-room
    - bedroom-3

    Each event must include:
    - time_raw
    - location
    - event_summary
    - entities
    - urgency

    Transcript:
    ---
    {transcript}
    ---
    """

    return call_custom_llm_api(prompt)


def generate_summary_with_llm(transcript: str) -> str:
    prompt = f"""
    Summarize the following emergency radio transcript into a concise,
    professional after-action report paragraph.

    Transcript:
    ---
    {transcript}
    ---
    """

    return call_custom_llm_api(prompt)
