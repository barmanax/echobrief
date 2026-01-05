import os
import json
import shutil
import re
from collections import defaultdict

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from transcription import transcribe_audio
from intelligence import extract_events_with_llm, generate_summary_with_llm

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


def parse_time_to_seconds(time_str: str) -> int:
    match = re.search(r"(\d{1,2}):(\d{2})", str(time_str))
    if not match:
        return 0
    return int(match.group(1)) * 60 + int(match.group(2))


@app.post("/api/process-incident/")
async def process_incident(audio_file: UploadFile = File(...)):
    try:
        audio_path = os.path.join(UPLOADS_DIR, audio_file.filename)

        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        transcript = transcribe_audio(audio_path)

        events_raw = extract_events_with_llm(transcript)
        events = json.loads(events_raw)

        summary = generate_summary_with_llm(transcript)

        officer_contributions = defaultdict(list)

        for event in events:
            event["timestamp_sec"] = parse_time_to_seconds(
                event.get("time_raw", "00:00")
            )

            for entity in event.get("entities", []):
                officer_contributions[entity].append(event["event_summary"])

        os.remove(audio_path)

        return {
            "events": events,
            "incidentSummary": summary,
            "officerContributions": dict(officer_contributions),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
