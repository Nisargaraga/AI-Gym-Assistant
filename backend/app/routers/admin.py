from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Workout, Habit

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db)
):

    return {
        "total_users":
            db.query(User).count(),

        "total_workouts":
            db.query(Workout).count(),

        "total_habits":
            db.query(Habit).count()
    }