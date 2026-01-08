import React, { useState, useEffect, useMemo, useRef } from "react";
import axios from "axios";
import SVG from "react-inlinesvg";
import {
  FaDoorOpen,
  FaExclamationTriangle,
  FaCheckCircle,
  FaUserShield,
  FaTimes,
  FaPlay,
  FaPause,
} from "react-icons/fa";
import "./App.css";

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [audioSrc, setAudioSrc] = useState(null);
  const [floorplanSvg, setFloorplanSvg] = useState("");

  const [events, setEvents] = useState([]);
  const [incidentSummary, setIncidentSummary] = useState("");
  const [officerContributions, setOfficerContributions] = useState({});
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [roomCoords, setRoomCoords] = useState({});

  const [isLoading, setIsLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const audioRef = useRef(null);
  const visualPanelRef = useRef(null);

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

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    setAudioFile(file);
    if (audioSrc) URL.revokeObjectURL(audioSrc);
    setAudioSrc(URL.createObjectURL(file));
  };

  const handleFloorplanChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (evt) => setFloorplanSvg(evt.target.result);
    reader.readAsText(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!audioFile || !floorplanSvg) {
      alert("Please upload both files.");
      return;
    }

    setIsLoading(true);
    setEvents([]);
    setIncidentSummary("");
    setOfficerContributions({});
    setSelectedEvent(null);

    const formData = new FormData();
    formData.append("audio_file", audioFile);

    try {
      const res = await axios.post(
        "http://localhost:8000/api/process-incident/",
        formData
      );
      setEvents(res.data.events);
      setIncidentSummary(res.data.incidentSummary);
      setOfficerContributions(res.data.officerContributions);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayPause = () => {
    if (!audioRef.current) return;
    isPlaying ? audioRef.current.pause() : audioRef.current.play();
  };

  const handleSeek = (time) => {
    if (!audioRef.current) return;
    audioRef.current.currentTime = time;
    setCurrentTime(time);
  };

  const handleIconClick = (event) => {
    setSelectedEvent(event);
    const seekTime = ROOM_TIMESTAMPS[event.location] || 0;
    handleSeek(seekTime);
  };

  const significantRoomEvents = useMemo(() => {
    const urgencyOrder = { high: 3, medium: 2, low: 1 };
    const map = {};
    for (const e of events) {
      if (!e.location) continue;
      if (
        !map[e.location] ||
        urgencyOrder[e.urgency] > urgencyOrder[map[e.location].urgency]
      ) {
        map[e.location] = e;
      }
    }
    return Object.values(map);
  }, [events]);

  const getIconForEvent = (event) => {
    const s = event.event_summary.toLowerCase();
    if (s.includes("ransacked") || s.includes("crime"))
      return <FaExclamationTriangle />;
    if (s.includes("entry")) return <FaDoorOpen />;
    if (s.includes("clear")) return <FaCheckCircle />;
    return <FaUserShield />;
  };

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;
    const onTime = () => setCurrentTime(audio.currentTime);
    const onMeta = () => setDuration(audio.duration);
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", onTime);
    audio.addEventListener("loadedmetadata", onMeta);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);

    return () => {
      audio.removeEventListener("timeupdate", onTime);
      audio.removeEventListener("loadedmetadata", onMeta);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
    };
  }, [audioSrc]);

  useEffect(() => {
    if (!visualPanelRef.current) return;
    const containerRect = visualPanelRef.current.getBoundingClientRect();
    const coords = {};

    significantRoomEvents.forEach((e) => {
      const el = document.getElementById(e.location);
      if (!el) return;
      const r = el.getBoundingClientRect();
      coords[e.location] = {
        x: r.left + r.width / 2 - containerRect.left,
        y: r.top + r.height / 2 - containerRect.top,
      };
    });

    setRoomCoords(coords);
  }, [significantRoomEvents, floorplanSvg]);

  return (
    <div className="App">
      <audio ref={audioRef} src={audioSrc} />

      {}
    </div>
  );
}

export default App;
