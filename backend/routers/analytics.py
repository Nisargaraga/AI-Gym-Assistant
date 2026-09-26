from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
import schemas
from datetime import datetime, timedelta
router = APIRouter(prefix="/analytics", tags=["Performance & Analytics"])
@router.get("/dashboard")
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retrieves aggregated summary statistics for the user overview panel.
    """
    # 1. Calculate workout streak
    # Get last habit entry
    recent_habit = db.query(models.HabitTracking).filter(
        models.HabitTracking.user_id == current_user.id
    ).order_by(models.HabitTracking.created_at.desc()).first()
    
    streak = recent_habit.streak_days if recent_habit else 1
    # 2. Get today's logged calories
    day_str = datetime.now().strftime("%a")
    today_calories_log = db.query(models.DietLog).filter(
        models.DietLog.user_id == current_user.id,
        models.DietLog.date == day_str
    ).all()
    
    today_calories = sum(log.calories_consumed for log in today_calories_log)
    
    # Calculate calorie target
    target_calories = 2000
    if current_user.goal == "bulk":
        target_calories = int(2400 + (current_user.weight - 70) * 10)
    elif current_user.goal == "lean":
        target_calories = int(1800 + (current_user.weight - 70) * 5)
    # 3. Calculate BMI
    height_meters = current_user.height / 100.0
    bmi = round(current_user.weight / (height_meters ** 2), 1) if height_meters > 0 else 0.0
    # 4. Total active minutes in the last week
    recent_workouts = db.query(models.WorkoutHistory).filter(
        models.WorkoutHistory.user_id == current_user.id
    ).limit(7).all()
    
    total_active_mins = sum(w.duration for w in recent_workouts)
    # 5. Compile weekly history for SVG chart drawing
    # Default week template
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    history_map = {day: {"date": day, "reps": 0, "duration": 0, "performance": 0} for day in week_days}
    
    for w in recent_workouts:
        if w.date in history_map:
            history_map[w.date]["reps"] += w.reps
            history_map[w.date]["duration"] += w.duration
            history_map[w.date]["performance"] = int(max(history_map[w.date]["performance"], w.performance_score))
    history_list = [history_map[d] for d in week_days]
    # Calculate overall scores
    avg_form = sum(w.form_score for w in recent_workouts) / len(recent_workouts) if recent_workouts else 80.0
    avg_endurance = sum(w.endurance_score for w in recent_workouts) / len(recent_workouts) if recent_workouts else 75.0
    avg_consistency = (len(recent_workouts) / 7.0) * 100.0 if recent_workouts else 50.0
    
    # Overall Performance Score
    overall_performance = (avg_form * 0.4) + (avg_endurance * 0.3) + (avg_consistency * 0.3)
    return {
        "streak_days": streak,
        "bmi": bmi,
        "weight": current_user.weight,
        "height": current_user.height,
        "today_calories": today_calories,
        "target_calories": target_calories,
        "active_minutes": total_active_mins,
        "workout_history": history_list,
        "performance_scores": {
            "overall": round(overall_performance, 1),
            "form": round(avg_form, 1),
            "consistency": round(avg_consistency, 1),
            "endurance": round(avg_endurance, 1)
        }
    }
