import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from auth import get_current_user
from services.gemini_service import GeminiService
import models
import schemas
router = APIRouter(prefix="/dietician", tags=["Dietician & Calorie Coach"])
@router.post("/", response_model=dict)
async def query_dietician(
    query_in: schemas.GymBuddyChatCreate,
    api_key: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Retrieve user's recent logs to feed into Gemini context
    recent_logs = db.query(models.DietLog).filter(
        models.DietLog.user_id == current_user.id
    ).order_by(models.DietLog.created_at.desc()).limit(3).all()
    
    formatted_logs = [
        {"food": log.food_items, "calories": log.calories_consumed, "date": log.date}
        for log in recent_logs
    ]
    user_profile = {
        "name": current_user.name,
        "weight": current_user.weight,
        "height": current_user.height,
        "goal": current_user.goal,
        "diet_preference": current_user.diet_preference
    }
    # Generate reply using Gemini service
    reply_text = await GeminiService.generate_diet_plan(
        query=query_in.message,
        user_profile=user_profile,
        history_logs=formatted_logs,
        api_key=api_key
    )
    # Smart calorie extraction (NLP parsing)
    # Check if the user is trying to log a meal, e.g., "log 500 calories", "ate a chicken wrap 600 cal"
    query_lower = query_in.message.lower()
    is_log_intent = any(kw in query_lower for kw in ["log", "ate", "eat", "consumed", "add meal"])
    
    if is_log_intent:
        # Match digits followed by calories/cal/kcal/cals
        cal_match = re.search(r"(\d+)\s*(calorie|cal|kcal)", query_lower)
        calories = 0
        food_item = "Logged Meal"
        
        if cal_match:
            calories = int(cal_match.group(1))
        else:
            # Default calorie mapping for common foods if no exact number matches
            if "apple" in query_lower or "banana" in query_lower:
                calories = 95
                food_item = "Fruit (Apple/Banana)"
            elif "shake" in query_lower or "protein" in query_lower:
                calories = 220
                food_item = "Protein Shake"
            elif "chicken" in query_lower or "rice" in query_lower:
                calories = 550
                food_item = "Chicken & Rice Meal"
            elif "salad" in query_lower:
                calories = 180
                food_item = "Garden Salad"
            elif "pizza" in query_lower or "burger" in query_lower:
                calories = 800
                food_item = "Fast Food Cheat Meal"
        if calories > 0:
            # Create a diet log entry automatically!
            # Day of the week
            day_str = datetime.now().strftime("%a")
            # Calculate target calories based on user weight and goal
            target = 2000
            if current_user.goal == "bulk":
                target = int(2400 + (current_user.weight - 70) * 10)
            elif current_user.goal == "lean":
                target = int(1800 + (current_user.weight - 70) * 5)
            
            new_log = models.DietLog(
                user_id=current_user.id,
                date=day_str,
                calories_consumed=calories,
                calories_target=target,
                food_items=food_item,
                protein=int(calories * 0.25 / 4),  # estimate macros roughly
                carbs=int(calories * 0.5 / 4),
                fat=int(calories * 0.25 / 9)
            )
            db.add(new_log)
            db.commit()
    return {"response": reply_text}
@router.post("/logs", response_model=schemas.DietLogResponse)
def create_diet_log(
    log_in: schemas.DietLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    day_str = log_in.date or datetime.now().strftime("%a")
    new_log = models.DietLog(
        user_id=current_user.id,
        date=day_str,
        calories_consumed=log_in.calories_consumed,
        calories_target=log_in.calories_target,
        food_items=log_in.food_items,
        protein=log_in.protein,
        carbs=log_in.carbs,
        fat=log_in.fat
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
@router.get("/logs", response_model=List[schemas.DietLogResponse])
def get_diet_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.DietLog).filter(
        models.DietLog.user_id == current_user.id
    ).order_by(models.DietLog.created_at.desc()).all()