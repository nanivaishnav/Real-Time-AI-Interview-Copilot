# backend/speech_to_text.py
import sounddevice as sd
from scipy.io.wavfile import write
import queue
from llm_service import transcribe, transcribe_audio_chunk

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def record_audio(filename="input.wav", duration=5, fs=16000):
    """
    Record audio for fixed duration and save as WAV
    """
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Recording saved:", filename)

def start_streaming():
    """
    Real-time streaming transcription
    """
    stream = sd.InputStream(samplerate=16000, channels=1, callback=audio_callback)
    with stream:
        print("Streaming audio... Press Ctrl+C to stop.")
        while True:
            audio_chunk = audio_queue.get()
            text = transcribe_audio_chunk(audio_chunk)
            print("Transcribed text:", text)