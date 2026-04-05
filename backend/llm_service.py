# backend/llm_service.py
import os
from openai import OpenAI
from dotenv import load_dotenv
import whisper
import io
import soundfile as sf
import numpy as np

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Whisper model for offline transcription
whisper_model = whisper.load_model("small")

def analyze_answer(user_answer: str):
    """
    Sends user answer to OpenAI GPT for feedback
    """
    prompt = f"""
    You are an interview coach.

    Analyze this answer:
    "{user_answer}"

    Give:
    1. Feedback (clarity, depth, missing points)
    2. Improved version of the answer
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def transcribe(audio_path):
    """
    Transcribe a WAV file using Whisper
    """
    result = whisper_model.transcribe(audio_path)
    return result["text"]

def transcribe_audio_chunk(audio_chunk, sample_rate=16000):
    """
    Transcribe a numpy audio chunk (real-time streaming)
    """
    with io.BytesIO() as f:
        sf.write(f, audio_chunk, sample_rate, format='WAV')
        f.seek(0)
        # Use OpenAI Whisper API (optional) if you want cloud transcription
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript['text']