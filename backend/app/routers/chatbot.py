import os

from fastapi import APIRouter
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Gym Buddy"]
)

@router.post("/message")
def chat(message: str):

    prompt = f"""
You are an AI Fitness Coach.

Help users with:
- Weight Loss
- Muscle Gain
- Diet Planning
- Workout Plans
- Motivation
- Fitness Habits

User Question:
{message}
"""

    response = model.generate_content(
        prompt
    )

    return {
        "user_message": message,
        "reply": response.text
    }