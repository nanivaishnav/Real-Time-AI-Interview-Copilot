import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("**** **** *** *** **** ****"))

def analyze_answer(user_answer: str):
    prompt = f"""s
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
