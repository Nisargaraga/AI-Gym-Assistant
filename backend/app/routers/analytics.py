from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Workout, Habit

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/{user_id}")
def get_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    workouts = (
        db.query(Workout)
        .filter(Workout.user_id == user_id)
        .all()
    )

    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .all()
    )

    total_workouts = len(workouts)

    avg_accuracy = 0

    if total_workouts > 0:
        avg_accuracy = (
            sum(w.accuracy for w in workouts)
            / total_workouts
        )

    return {
        "name": user.name,
        "goal": user.goal,
        "total_workouts": total_workouts,
        "average_accuracy": round(avg_accuracy, 2),
        "habit_records": len(habits)
    }