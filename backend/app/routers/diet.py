import random
from fastapi import APIRouter

router = APIRouter(
    prefix="/diet",
    tags=["Diet AI"]
)

@router.post("/plan")
def generate_diet_plan(
    weight: float,
    height: float,
    goal: str,
    diet_preference: str
):

    bmi = weight / ((height / 100) ** 2)

    if goal.lower() == "weight loss":
        calories = weight * 22

        veg_plans = [
            {
                "breakfast": "Oats + Apple",
                "lunch": "Brown Rice + Dal + Salad",
                "dinner": "Vegetable Soup + Paneer"
            },
            {
                "breakfast": "Poha + Green Tea",
                "lunch": "Chapati + Mixed Vegetables",
                "dinner": "Salad + Sprouts"
            }
        ]

        nonveg_plans = [
            {
                "breakfast": "Boiled Eggs + Toast",
                "lunch": "Grilled Chicken + Rice",
                "dinner": "Fish + Salad"
            },
            {
                "breakfast": "Egg Omelette",
                "lunch": "Chicken Breast + Vegetables",
                "dinner": "Soup + Fish"
            }
        ]

    elif goal.lower() == "muscle gain":
        calories = weight * 35

        veg_plans = [
            {
                "breakfast": "Milk + Banana + Peanut Butter",
                "lunch": "Rice + Dal + Paneer",
                "dinner": "Chapati + Paneer Curry"
            },
            {
                "breakfast": "Oats + Dry Fruits",
                "lunch": "Rajma + Rice",
                "dinner": "Paneer + Vegetables"
            }
        ]

        nonveg_plans = [
            {
                "breakfast": "Eggs + Milk",
                "lunch": "Chicken + Rice",
                "dinner": "Fish + Potatoes"
            },
            {
                "breakfast": "Omelette + Banana",
                "lunch": "Chicken Breast + Rice",
                "dinner": "Eggs + Vegetables"
            }
        ]

    else:
        calories = weight * 28

        veg_plans = [
            {
                "breakfast": "Idli + Sambar",
                "lunch": "Rice + Dal",
                "dinner": "Chapati + Vegetables"
            }
        ]

        nonveg_plans = [
            {
                "breakfast": "Eggs + Toast",
                "lunch": "Chicken + Rice",
                "dinner": "Fish + Vegetables"
            }
        ]

    if diet_preference.lower() == "vegetarian":
        diet_plan = random.choice(veg_plans)
    else:
        diet_plan = random.choice(nonveg_plans)

    return {
        "BMI": round(bmi, 2),
        "Target Calories": round(calories),
        "Diet Plan": diet_plan
    }