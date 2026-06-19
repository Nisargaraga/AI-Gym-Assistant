from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    weight: float
    height: float
    goal: str
    diet_preference: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        from_attributes = True


class WorkoutCreate(BaseModel):
    user_id: int
    exercise: str
    reps: int
    accuracy: float


class HabitCreate(BaseModel):
    user_id: int
    streak: int
    missed_days: int
    prediction: str