import React, { useState, useEffect, useMemo, useRef } from "react";
import axios from "axios";
import SVG from "react-inlinesvg";
import "./App.css";
import {
  FaDoorOpen,
  FaExclamationTriangle,
  FaCheckCircle,
  FaUserShield,
  FaTimes,
  FaPlay,
  FaPause,
} from "react-icons/fa";

const Timeline = ({ duration, events, currentTime, onSeek }) => {
  if (duration === 0) return null;

  const handleSeek = (e) => {
    const timeline = e.currentTarget;
    const rect = timeline.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const seekRatio = clickX / rect.width;
    onSeek(seekRatio * duration);
  };

  return (
    <div className="timeline-container-visual" onClick={handleSeek}>
      <div className="timeline-track">
        {events.map((event) => (
          <div
            key={event.timestamp_sec + event.event_summary}
            className={`event-marker urgency-${event.urgency}`}
            style={{ left: `${(event.timestamp_sec / duration) * 100}%` }}
            title={`${event.time_raw} - ${event.event_summary}`}
          />
        ))}
        <div
          className="timeline-handle"
          style={{ left: `${(currentTime / duration) * 100}%` }}
        />
      </div>
    </div>
  );
};

function App() {
  const [events, setEvents] = useState([]);
  const [incidentSummary, setIncidentSummary] = useState("");
  const [officerContributions, setOfficerContributions] = useState({});
  const [roomCoords, setRoomCoords] = useState({});
  const [selectedEvent, setSelectedEvent] = useState(null);

  const [audioFile, setAudioFile] = useState(null);
  const [floorplanSvg, setFloorplanSvg] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const audioRef = useRef(null);
  const [audioSrc, setAudioSrc] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const visualPanelRef = useRef(null);

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    setAudioFile(file);

    if (audioSrc) URL.revokeObjectURL(audioSrc);
    setAudioSrc(URL.createObjectURL(file));
  };

  const ROOM_TIMESTAMPS = {
    entrance: 31,
    bathroom: 36,
    "dining-room": 46,
    "bedroom-1": 56,
    "tv-room": 62,
    "bedroom-2": 65,
    "living-room": 94,
    "bedroom-3": 95,
  };

  const handleFloorplanChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => setFloorplanSvg(event.target.result);
      reader.readAsText(file);
    }
  };

  // (More App.js continues — upload next screenshots and I’ll keep appending cleanly.)
}

export default App;
