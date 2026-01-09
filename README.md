# EchoBrief

**EchoBrief** is an AI-powered post-incident analysis tool that transforms raw emergency radio traffic into structured, visual after-action briefings. It combines speech-to-text, large language models, and interactive visualizations to dramatically reduce the time required for incident review.

---

## 🚨 Problem

After critical incidents, responders must manually review long radio recordings to reconstruct:
- What happened  
- When it happened  
- Where it happened  
- Who was involved  

This process is slow, error-prone, and cognitively demanding — especially under time pressure.

---

## 💡 Solution

EchoBrief automates post-incident analysis by:
1. **Transcribing radio traffic**
2. **Extracting structured events with timestamps, locations, and urgency**
3. **Generating a concise incident summary**
4. **Visualizing events on a floorplan synced to the audio timeline**

The result is a single, interactive dashboard that replaces hours of manual review.

---

## ✨ Key Features

- 🎙 **Automatic Transcription**  
  Uses OpenAI Whisper to convert radio audio into text.

- 🧠 **LLM-Powered Event Extraction**  
  Extracts timestamped events, normalized locations, urgency levels, and involved units.

- 📝 **Incident Summary Generation**  
  Produces a professional after-action summary paragraph.

- 🗺 **Interactive Floorplan Overlay**  
  Events are mapped directly onto a building floorplan with urgency-coded icons.

- ⏱ **Audio–Timeline Synchronization**  
  Clicking an event seeks the audio to the corresponding moment.

- 👮 **Officer Contribution Breakdown**  
  Automatically groups actions by responding unit or officer.

---

## 🧱 Architecture Overview

```
Audio (.wav)
   ↓
Whisper Transcription
   ↓
LLM Event Extraction + Summary
   ↓
FastAPI Backend (JSON API)
   ↓
React Frontend Dashboard
```

---

## 🖥 Tech Stack

### Frontend
- React (React 18)
- JavaScript
- Axios
- React Icons
- SVG rendering

### Backend
- FastAPI (Python)
- OpenAI Whisper
- Large Language Model API

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- FFmpeg

---

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_KEY=your_api_key_here
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

App runs at:  
http://localhost:3000

---

## 🧪 Usage

1. Upload an incident radio recording
2. Upload a floorplan SVG
3. Click **Generate Briefing**
4. Explore the dashboard

---

## 🏆 Achievements

- **Top 10 Project** out of 495 submissions  
  Motorola Solutions Project Greenlight

- Reduced manual review time by ~70%

---

## 📈 Future Work

- Real-time streaming analysis
- Multi-floor support
- Exportable reports
- CAD / RMS integration

---

## 👤 Author

**Aditya Barman**  
Computer Science & Statistics @ UIUC
