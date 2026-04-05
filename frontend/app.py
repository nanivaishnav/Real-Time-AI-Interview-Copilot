import streamlit as st
import requests

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
