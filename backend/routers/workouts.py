from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_user
from services.pose_service import PoseService
from services.recommendation_service import RecommendationService
from services.gemini_service import GeminiService
import models
import schemas
router = APIRouter(prefix="/workouts", tags=["Workouts & Recommender"])
@router.post("/", response_model=schemas.WorkoutResponse)
def log_workout(
    workout_in: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Calculate scores on the backend using the PoseService
    scores = PoseService.calculate_session_scores(
        exercise=workout_in.exercise,
        reps=workout_in.reps,
        duration_minutes=workout_in.duration
    )
    # Check if there is already an entry for this day to keep history neat
    existing = db.query(models.WorkoutHistory).filter(
        models.WorkoutHistory.user_id == current_user.id,
        models.WorkoutHistory.date == workout_in.date
    ).first()
    if existing:
        # Update existing record
        existing.exercise = workout_in.exercise
        existing.reps += workout_in.reps
        existing.duration += workout_in.duration
        # Recalculate scores with aggregated reps/duration
        aggregated_scores = PoseService.calculate_session_scores(
            exercise=existing.exercise,
            reps=existing.reps,
            duration_minutes=existing.duration
        )
        existing.performance_score = aggregated_scores["performance_score"]
        existing.form_score = aggregated_scores["form_score"]
        existing.consistency_score = aggregated_scores["consistency_score"]
        existing.endurance_score = aggregated_scores["endurance_score"]
        db.commit()
        db.refresh(existing)
        return existing
    # Create new workout log
    workout = models.WorkoutHistory(
        user_id=current_user.id,
        date=workout_in.date,
        exercise=workout_in.exercise,
        reps=workout_in.reps,
        duration=workout_in.duration,
        performance_score=scores["performance_score"],
        form_score=scores["form_score"],
        consistency_score=scores["consistency_score"],
        endurance_score=scores["endurance_score"]
    )
    db.add(workout)
    
    # Update user's streak in habits if available
    habit = db.query(models.HabitTracking).filter(
        models.HabitTracking.user_id == current_user.id,
        models.HabitTracking.date == workout_in.date
    ).first()
    if habit:
        habit.workout_completed = True
        
    db.commit()
    db.refresh(workout)
    return workout
@router.get("/", response_model=List[schemas.WorkoutResponse])
def get_workouts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.WorkoutHistory).filter(
        models.WorkoutHistory.user_id == current_user.id
    ).all()
@router.get("/planner")
async def get_workout_planner(
    level: str = "beginner",
    api_key: str = None,
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate a 7-day program using Gemini if key is provided, or fallback to recommendation service config.
    """
    user_profile = {
        "name": current_user.name,
        "weight": current_user.weight,
        "height": current_user.height,
        "goal": current_user.goal
    }
    
    # Try calling Gemini to generate a dynamic weekly plan, fallback is handled in gemini_service
    plan = await GeminiService.generate_workout_plan(user_profile, level, api_key)
    structured_info = RecommendationService.get_program_details(level, current_user.goal)
    
    return {
        "program_details": structured_info,
        "weekly_plan_markdown": plan
    }
@router.get("/gyms")
def get_gym_recommendations(
    current_user: models.User = Depends(get_current_user)
):
    return RecommendationService.get_nearby_gyms(current_user.goal)