import shutil
import os
import json
import re

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

from transcription import transcribe_audio_with_whisper
from intelligence import extract_events_with_gemini, generate_summary_with_gemini

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = "temp_uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)


# --- THIS IS THE UPDATED, MORE ROBUST FUNCTION ---
def parse_time_to_seconds(time_str: str) -> int:
    """
    More robustly converts a 'MM:SS' string or similar to total seconds.
    It now handles extra characters and variations by searching for the pattern.
    """
    try:
        # Use regex to find the first occurrence of a MM:SS or M:SS pattern
        match = re.search(r"(\d{1,2}):(\d{2})", str(time_str))
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            return minutes * 60 + seconds
        return 0
    except:
        return 0


@app.post("/api/process-incident/")
async def process_incident(audio_file: UploadFile = File(...)):
    try:
        audio_path = os.path.join(UPLOADS_DIR, audio_file.filename)
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        transcript = transcribe_audio_with_whisper(audio_path)

        events_json_str = extract_events_with_gemini(transcript)
        events = json.loads(events_json_str)

        incident_summary = generate_summary_with_gemini(transcript)

        officer_contributions = defaultdict(list)

        for event in events:
            # This will now use the more robust parser
            event["timestamp_sec"] = parse_time_to_seconds(event.get("time_raw", "00:00"))

            for entity in event.get("entities", []):
                officer_contributions[entity].append(event["event_summary"])

        os.remove(audio_path)

        # Print the processed events on the backend to help debug
        print("\n--- Processed Events Sent to Frontend ---")
        print(json.dumps(events, indent=2))
        print("----------------------------------------\n")

        return {
            "events": events,
            "incidentSummary": incident_summary,
            "officerContributions": dict(officer_contributions),
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
