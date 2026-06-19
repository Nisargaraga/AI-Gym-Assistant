from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Workout
from ..schemas import WorkoutCreate

router = APIRouter(
    prefix="/workout",
    tags=["Workout AI"]
)

@router.post("/log")
def log_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):

    new_workout = Workout(
        user_id=workout.user_id,
        exercise=workout.exercise,
        reps=workout.reps,
        accuracy=workout.accuracy
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    performance_score = (
        workout.accuracy * 0.7
        +
        min(workout.reps, 20) * 1.5
    )

    if performance_score > 90:
        rating = "Excellent"

    elif performance_score > 70:
        rating = "Good"

    else:
        rating = "Needs Improvement"

    return {
        "message": "Workout Logged",
        "performance_score": round(performance_score, 2),
        "rating": rating
    }


@router.get("/history/{user_id}")
def workout_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .all()
    )

    return workouts