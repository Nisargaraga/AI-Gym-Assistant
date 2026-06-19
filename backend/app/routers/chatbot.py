import os

from fastapi import APIRouter
from dotenv import load_dotenv

import google.generativeai as genai

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Use a model that your API key supports
model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Gym Buddy"]
)


@router.post("/message")
def chat(message: str):

    try:

        prompt = f"""
You are an expert AI Fitness Coach.

Help users with:
- Weight Loss
- Muscle Gain
- Diet Planning
- Workout Routines
- Fitness Motivation
- Healthy Habits

Provide practical and easy-to-understand fitness advice.

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

    except Exception as e:

     error = str(e)

    if "quota" in error.lower():

        return {
            "user_message": message,
            "reply": """
Gemini API quota exceeded.

Fitness Tip:
Stay consistent with workouts,
eat sufficient protein,
sleep 7-8 hours daily,
and maintain proper hydration.
"""
        }

    return {
        "user_message": message,
        "reply": f"Error: {error}"
    }