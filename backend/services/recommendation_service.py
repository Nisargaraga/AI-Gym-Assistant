from typing import List, Dict
from services.gemini_service import GeminiService
class RecommendationService:
    @staticmethod
    def get_program_details(level: str, goal: str) -> Dict:
        """
        Standardized offline program planner configs.
        """
        programs = {
            "beginner": {
                "name": "Foundational Fitness",
                "frequency": "3 Days / Week",
                "focus": "Form & Joint Mobility",
                "description": "Perfect for establishing consistency and learning basic movement patterns.",
                "schedule": [
                    {"day": "Monday", "activity": "Bodyweight Squats (3x10), Light Walk (15m)", "type": "Strength & Recovery"},
                    {"day": "Wednesday", "activity": "Bicep Curls (3x8), Push-ups (3x5), Core plank (3x30s)", "type": "Upper & Core"},
                    {"day": "Friday", "activity": "Spin-Bike Telemetry Cycle (15m at gear 4)", "type": "Cardio"}
                ]
            },
            "intermediate": {
                "name": "Volume Builder",
                "frequency": "4 Days / Week",
                "focus": "Hypertrophy & Aerobic Base",
                "description": "Designed to increase muscular endurance and capacity.",
                "schedule": [
                    {"day": "Monday", "activity": "Squats (4x15), Lunges (3x12), Active stretch", "type": "Lower Body"},
                    {"day": "Tuesday", "activity": "Spin-Bike Interval (20m, alternate gears 5 & 10)", "type": "Cardio HIIT"},
                    {"day": "Thursday", "activity": "Bicep Curls (4x12), Push-ups (4x12), Plank (3x60s)", "type": "Upper Body Focus"},
                    {"day": "Saturday", "activity": "Steady Cardio Ride (30m, gear 6, target 130 BPM)", "type": "Endurance"}
                ]
            },
            "advanced": {
                "name": "Elite Athlete",
                "frequency": "5-6 Days / Week",
                "focus": "Power, Strength & Maximum Capacity",
                "description": "High density sessions targeting absolute performance thresholds.",
                "schedule": [
                    {"day": "Monday", "activity": "Squats (5x20), Plyometric jumps, Weighted lunges", "type": "Lower Explosiveness"},
                    {"day": "Tuesday", "activity": "HIIT Sprint Pedaling (25m, peaks at 300W)", "type": "Biometric Power"},
                    {"day": "Wednesday", "activity": "Push-up failure sets, Curls (5x15), Core leg raises", "type": "Upper Hypertrophy"},
                    {"day": "Friday", "activity": "Full-body metabolic conditioning circuit", "type": "Conditioning"},
                    {"day": "Saturday", "activity": "Long duration aerobic spin (45m, gear 8)", "type": "LSD Cardio"}
                ]
            }
        }
        return programs.get(level.lower(), programs["beginner"])
    @staticmethod
    def get_nearby_gyms(goal: str) -> List[Dict]:
        """
        Returns a list of local gym partners based on user fitness goal.
        """
        all_gyms = [
            {
                "name": "Apex Iron Gym",
                "type": "strength",
                "distance": "1.2 km",
                "rating": 4.8,
                "perks": "Powerlifting racks, heavy dumbbells, turf area",
                "offer": "Free 1-Day Pass"
            },
            {
                "name": "Vibe Health & Yoga",
                "type": "yoga",
                "distance": "2.4 km",
                "rating": 4.9,
                "perks": "Hot yoga studio, recovery sauna, juice bar",
                "offer": "15% off first month"
            },
            {
                "name": "Pulse Fitness Center",
                "type": "cardio",
                "distance": "0.8 km",
                "rating": 4.5,
                "perks": "Smart spin bikes, rowing machines, pool",
                "offer": "Free 3-Day Guest Pass"
            },
            {
                "name": "CrossFit Obsidian",
                "type": "crossfit",
                "distance": "3.1 km",
                "rating": 4.7,
                "perks": "Olympic lifting, HIIT coaching, community class",
                "offer": "Intro class for $10"
            }
        ]
        
        # Sort based on goal preferences
        if goal == "bulk":
            return [g for g in all_gyms if g["type"] in ["strength", "crossfit"]] + [g for g in all_gyms if g["type"] not in ["strength", "crossfit"]]
        elif goal == "lean":
            return [g for g in all_gyms if g["type"] in ["cardio", "crossfit"]] + [g for g in all_gyms if g["type"] not in ["cardio", "crossfit"]]
        else:
            return all_gyms
