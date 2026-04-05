import streamlit as st
import requests
import streamlit as st
import websocket
import threading
# frontend/app.py
import streamlit as st
import websocket
import threading
# frontend/app.py
import streamlit as st
from backend.speech_to_text import record_audio, transcribe
from backend.llm_service import analyze_answer


st.title("🎤 AI Interview Copilot (MVP)")

user_input = st.text_area("Enter your answer:")

if st.button("Analyze"):
    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={"answer": user_input}
    )

    if response.status_code == 200:
        st.write("### Feedback:")
        st.write(response.json()["result"])
    else:
        st.error("Error connecting to backend")

        st.title("🎤 AI Interview Copilot (Live Feedback)")

user_input = st.text_area("Speak or type your answer:")

if st.button("Start Live Feedback"):
    def run_ws():
        ws = websocket.WebSocket()
        ws.connect("ws://127.0.0.1:8000/ws/analyze")
        ws.send(user_input)
        while True:
            feedback = ws.recv()
            st.write("Feedback:", feedback)

    thread = threading.Thread(target=run_ws)
    thread.start()
st.title("🎤 AI Interview Copilot (Live Feedback)")

if st.button("Start Interview"):
    def run_ws():
        ws = websocket.WebSocket()
        ws.connect("ws://127.0.0.1:8000/ws/analyze")

        # Trigger backend to record audio
        ws.send("start recording")

        while True:
            response = ws.recv()
            st.write(response)

    thread = threading.Thread(target=run_ws)
    thread.start()

st.title("🎤 AI Interview Copilot (Speech MVP)")

# Button to record audio
if st.button("Record 5s"):
    st.info("Recording... speak now!")
    record_audio("input.wav", duration=5)
    st.success("Recording done!")

    # Convert speech → text
    text = transcribe("input.wav")
    st.write("You said:", text)

    # Send text to AI for analysis
    result = analyze_answer(text)
    st.write("Feedback:", result)