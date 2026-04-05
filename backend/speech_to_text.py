# backend/speech_to_text.py
import sounddevice as sd
from scipy.io.wavfile import write
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def record_audio(filename="input.wav", duration=5, fs=16000):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Recording saved:", filename)

def transcribe(audio_path):
    """
    Transcribe audio using OpenAI Whisper API
    """
    with open(audio_path, "rb") as f:
        transcript = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=f,
            api_key=OPENAI_API_KEY
        )
    return transcript["text"]