from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Habit
from ..schemas import HabitCreate

router = APIRouter(
    prefix="/habits",
    tags=["Habit Tracker"]
)

@router.post("/track")
def track_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db)
):

    new_habit = Habit(
        user_id=habit.user_id,
        streak=habit.streak,
        missed_days=habit.missed_days,
        prediction=habit.prediction
    )

    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)

    if habit.missed_days >= 3:
        risk = "High"

    elif habit.missed_days >= 1:
        risk = "Medium"

    else:
        risk = "Low"

    if risk == "High":
        motivation = "You are close to breaking your fitness habit. Start with a short workout today."

    elif risk == "Medium":
        motivation = "Stay consistent. One workout today keeps the streak alive."

    else:
        motivation = "Excellent consistency. Keep pushing forward."

    return {
        "risk_level": risk,
        "motivation": motivation
    }


@router.get("/{user_id}")
def get_habits(
    user_id: int,
    db: Session = Depends(get_db)
):
    habits = (
        db.query(Habit)
        .filter(Habit.user_id == user_id)
        .all()
    )

    return habits