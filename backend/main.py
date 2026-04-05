from fastapi import FastAPI
from pydantic import BaseModel
from llm_service import analyze_answer

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
