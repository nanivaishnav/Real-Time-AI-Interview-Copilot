# backend/main.py
from fastapi import FastAPI, WebSocket
from llm_service import analyze_answer
from speech_to_text import record_audio, transcribe

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Interview Copilot Backend Running"}

@app.websocket("/ws/analyze")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Frontend sends "start recording"
        data = await websocket.receive_text()

        # Record audio (5s for MVP)
        record_audio("input.wav", duration=5)

        # Convert audio → text
        user_text = transcribe("input.wav")
        await websocket.send_text(f"You said: {user_text}")

        # Send text to LLM
        feedback = analyze_answer(user_text)
        await websocket.send_text(f"Feedback: {feedback}")