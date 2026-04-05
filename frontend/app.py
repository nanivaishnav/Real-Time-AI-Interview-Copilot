# frontend/app.py
import streamlit as st
import websocket
import threading

st.title("🎤 AI Interview Copilot (Live Feedback)")

if st.button("Start Interview"):
    placeholder = st.empty()

    def run_ws():
        ws = websocket.WebSocket()
        ws.connect("ws://127.0.0.1:8000/ws/analyze")

        # Trigger backend to start recording
        ws.send("start recording")

        while True:
            response = ws.recv()
            placeholder.text(response)

    thread = threading.Thread(target=run_ws)
    thread.start()