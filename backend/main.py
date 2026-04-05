from fastapi import FastAPI
from pydantic import BaseModel
from llm_service import analyze_answer
from fastapi import FastAPI, WebSocket
from llm_service import analyze_answer
# backend/main.py
from fastapi import FastAPI, WebSocket
from llm_service import analyze_answer
from speech_to_text import transcribe, record_audio

app = FastAPI()

class AnswerRequest(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"message": "Interview Copilot API running"}

@app.post("/analyze")
def analyze(req: AnswerRequest):
    result = analyze_answer(req.answer)
    return {"result": result}
app = FastAPI()

@app.websocket("/ws/analyze")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Send partial feedback (can improve later with streaming API)
        result = analyze_answer(data)
        await websocket.send_text(result)
app = FastAPI()

@app.websocket("/ws/analyze")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive a trigger from frontend to record audio
        data = await websocket.receive_text()  # could be "start recording"

        # Record audio (for MVP, fixed 5s)
        record_audio("input.wav", duration=5)

        # Convert speech → text
        user_text = transcribe("input.wav")

        # Send text back to frontend so user can see what they said
        await websocket.send_text(f"You said: {user_text}")

        # Send text to LLM for analysis
        feedback = analyze_answer(user_text)

        # Send feedback back to frontend
        await websocket.send_text(f"Feedback: {feedback}")