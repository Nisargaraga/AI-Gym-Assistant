import os
import google.generativeai as genai
from typing import Optional
# Setup global client if key is in environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
class GeminiService:
    @staticmethod
    def get_model(api_key: Optional[str] = None):
        key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if key:
            try:
                genai.configure(api_key=key)
                # Use gemini-1.5-flash as the standard efficient model
                return genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                print(f"Error configuring Gemini: {e}")
        return None
    @classmethod
    async def generate_diet_plan(
        cls, query: str, user_profile: dict, history_logs: list, api_key: Optional[str] = None
    ) -> str:
        model = cls.get_model(api_key)
        
        system_prompt = (
            f"You are a certified AI Dietician & Calorie Coach in the GymFitGuide application.\n"
            f"User profile details:\n"
            f"- Name: {user_profile.get('name')}\n"
            f"- Weight: {user_profile.get('weight')} kg\n"
            f"- Height: {user_profile.get('height')} cm\n"
            f"- Goal: {user_profile.get('goal')}\n"
            f"- Diet Style: {user_profile.get('diet_preference')}\n"
            f"- Recent logs: {history_logs}\n\n"
            f"Provide encouraging, scientifically accurate, and structured advice. Use Markdown bolding and bullet lists when proposing menus or grocery lists. Keep response concise (under 250 words)."
        )
        if model:
            try:
                response = model.generate_content(
                    contents=[
                        {"role": "user", "parts": [f"System instructions:\n{system_prompt}\n\nUser request: {query}"]}
                    ]
                )
                return response.text
            except Exception as e:
                print(f"Gemini API Error: {e}")
                # Fallback to offline rule engine on API error
        
        return cls._offline_dietician_fallback(query, user_profile)
    @classmethod
    async def generate_buddy_chat(
        cls, message: str, user_profile: dict, chat_history: list, streak: int, api_key: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Returns (reply_text, vibe)
        """
        model = cls.get_model(api_key)
        
        system_prompt = (
            f"You are Flex, a Virtual Gym Buddy Chat Companion inside the GymFitGuide app.\n"
            f"Personality: Energetic, high-vibe, supportive, empathetic, friendly.\n"
            f"User Profile Details:\n"
            f"- Name: {user_profile.get('name')}\n"
            f"- Goal: {user_profile.get('goal')}\n"
            f"- Workout Streak: {streak} days\n\n"
            f"Guidelines:\n"
            f"- If the user expresses stress, exhaustion, or low motivation, match with an empathetic, recovery-focused tone.\n"
            f"- If the user is excited or preparing to train, boost their energy with a hyped tone.\n"
            f"- Keep the response brief (2-4 sentences max) and use emojis.\n"
            f"- Do not break character."
        )
        # Build conversation format for Gemini
        prompt_parts = [system_prompt, "\n\nChat History:"]
        for chat in chat_history[-6:]:  # include last 6 messages
            prompt_parts.append(f"{chat['sender']}: {chat['message']}")
        prompt_parts.append(f"user: {message}")
        prompt_parts.append("Flex:")
        prompt_str = "\n".join(prompt_parts)
        # Detect vibe from the input message
        query_lower = message.lower()
        vibe = "supportive"
        if any(kw in query_lower for kw in ["tired", "exhausted", "sleepy", "lazy", "skip", "sore", "weak", "no energy", "unmotivated"]):
            vibe = "empathetic"
        elif any(kw in query_lower for kw in ["ready", "excited", "let's go", "pumped", "strong", "gym", "crush", "workout", "train", "hype"]):
            vibe = "hyped"
        if model:
            try:
                response = model.generate_content(prompt_str)
                return response.text, vibe
            except Exception as e:
                print(f"Gemini API Error: {e}")
                # Fallback to offline buddy
        
        return cls._offline_buddy_fallback(message, user_profile, vibe), vibe
    @classmethod
    async def generate_workout_plan(
        cls, user_profile: dict, level: str, api_key: Optional[str] = None
    ) -> str:
        model = cls.get_model(api_key)
        system_prompt = (
            f"You are an expert fitness planner. Generate a highly customized weekly workout planner "
            f"for a user with target level '{level}'. User details: Weight: {user_profile.get('weight')}kg, "
            f"Height: {user_profile.get('height')}cm, Fitness goal: {user_profile.get('goal')}.\n"
            f"Provide a structured 7-day schedule with exercises, sets, reps, and brief instructions. "
            f"Keep it clean, readable, formatted in Markdown."
        )
        if model:
            try:
                response = model.generate_content(system_prompt)
                return response.text
            except Exception as e:
                print(f"Gemini API Error: {e}")
        # Fallback offline plan
        return cls._offline_plan_fallback(level, user_profile.get('goal', 'maintain'))
    # --- Offline Fallbacks ---
    @staticmethod
    def _offline_dietician_fallback(query: str, profile: dict) -> str:
        query_lower = query.lower()
        pref = profile.get("diet_preference", "balanced")
        goal = profile.get("goal", "maintain")
        weight = profile.get("weight", 70)
        # Quick structural responses
        if "meal plan" in query_lower or "diet plan" in query_lower or "eat" in query_lower:
            calories = 1800 if goal == "lean" else (2500 if goal == "bulk" else 2100)
            proteins = int(weight * (2.0 if goal == "bulk" else 1.6))
            fats = int((calories * 0.25) / 9)
            carbs = int((calories - (proteins * 4) - (fats * 9)) / 4)
            
            return (
                f"🥗 **Offline Mode Calorie Coach - target: {calories} kcal**\n\n"
                f"Macros split: Protein: **{proteins}g** | Carbs: **{carbs}g** | Fats: **{fats}g**\n"
                f"Style: **{pref.upper()}**\n\n"
                f"- **Breakfast**: Oats with almonds, banana slices, and protein supplement.\n"
                f"- **Lunch**: Leafy greens, grilled protein source (paneer/tofu/chicken), brown rice.\n"
                f"- **Snack**: Greek yogurt or soy yogurt with chia seeds.\n"
                f"- **Dinner**: Steamed veggies, baked sweet potato, olive oil dressing.\n\n"
                f"*Offline fallback triggered. Setup your GEMINI_API_KEY environment variable to enable dynamic AI dietician advice.*"
            )
        elif "grocery" in query_lower or "list" in query_lower or "shop" in query_lower:
            items = ["Whole Oats", "Leafy Greens (Spinach, Broccoli)", "Almonds / Chia seeds", "Sweet Potato & Brown Rice", "Tofu / Eggs / Chicken"]
            bullet_items = "\n".join([f"- [ ] {item}" for item in items])
            return (
                f"🛒 **Offline Smart Grocery Checklist**\n\n"
                f"{bullet_items}\n\n"
                f"*Offline fallback active. Please configure Gemini API key for smart meal itemization.*"
            )
        else:
            return (
                f"Hello {profile.get('name')}, I am running in Offline Mode. "
                f"Based on your profile, I recommend a daily intake of **{2200 if goal == 'bulk' else 1900} kcal** "
                f"to support your **{goal}** goal. Ask me for a 'meal plan' or a 'grocery list' to see schedules!"
            )
    @staticmethod
    def _offline_buddy_fallback(message: str, profile: dict, vibe: str) -> str:
        name = profile.get("name", "champ").split(" ")[0]
        if vibe == "empathetic":
            return (
                f"Hey {name}, I hear you. 🛌 It is totally fine to feel down or tired. "
                f"Your recovery is part of the process. Let's do a light 5-minute active recovery cycle today. "
                f"Showing up at 20% is better than not showing up at all! You got this."
            )
        elif vibe == "hyped":
            return (
                f"LET'S GO {name}! 🔥 That's what I am talking about! "
                f"The weights are waiting. Let's open the AI Gym Trainer and crush those rep goals. "
                f"I'm tracking your form, let's make it a legendary session! ⚡"
            )
        else:
            return (
                f"Hey {name}! 👋 Remember that consistency is what separates progress from plateau. "
                f"Whether it is a 10-minute stretch or a full lift, make today count! Let me know if you need a meal plan or a workout tip."
            )
    @staticmethod
    def _offline_plan_fallback(level: str, goal: str) -> str:
        return (
            f"# Weekly Workout Planner - {level.upper()} ({goal.upper()})\n\n"
            f"### Day 1: Strength - Lower Body Focus\n"
            f"- Squats: 3 sets x 10 reps (Focus on hip depth)\n"
            f"- Lunges: 3 sets x 12 reps\n"
            f"- Plank: 3 sets x 45 seconds\n\n"
            f"### Day 2: Cardio - High Intensity Intervals\n"
            f"- IoT Bike Pedaling: 15 mins (Alternate 1 min high resistance / 1 min low resistance)\n"
            f"- Jumping Jacks: 3 sets x 30 reps\n\n"
            f"### Day 3: Strength - Upper Body Focus\n"
            f"- Push-ups: 3 sets x max reps (Form symmetry focus)\n"
            f"- Bicep Curls: 3 sets x 12 reps (Full elbow extension)\n\n"
            f"### Day 4: Active Recovery & Mobility\n"
            f"- Light walking or yoga: 30 minutes\n"
            f"- Full body stretching\n\n"
            f"### Day 5: Strength - Full Body Workout\n"
            f"- Dumbbell Squats & Overhead Press: 3 sets x 10 reps\n"
            f"- Push-ups to plank transition: 3 sets x 10 reps\n\n"
            f"### Day 6: Cardio Endurance\n"
            f"- IoT Bike: Steady state cardiovascular pedaling (30 mins at level 5 resistance)\n\n"
            f"### Day 7: Fully Deserved Rest Day\n"
            f"- Focus on deep hydration and high protein intake."
        )