import whisper


def transcribe_audio_with_whisper(audio_path: str) -> str:
    """
    Transcribes an audio file using the local Whisper model.
    Returns the transcribed text as a single string.
    """
    print("Loading Whisper model (this may take a moment on first run)...")
    model = whisper.load_model("base")
    print("Whisper model loaded. Starting transcription...")

    result = model.transcribe(audio_path, fp16=False)  # fp16=False for CPU-only compatibility
    transcribed_text = result["text"]

    print("Transcription complete.")
    return transcribed_text
