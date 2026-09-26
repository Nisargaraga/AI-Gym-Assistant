from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None
# User Schemas
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
    weight: float
    height: float
    goal: str
    diet_preference: str
    status: str
    is_admin: bool
    created_at: datetime
    class Config:
        from_attributes = True
class UserProfileUpdate(BaseModel):
    name: str
    weight: float
    height: float
    goal: str
    diet_preference: str
class AdminUserUpdate(BaseModel):
    status: str  # Active, Suspended
    is_admin: Optional[bool] = None
# Workout Schemas
class WorkoutCreate(BaseModel):
    date: str
    exercise: str
    reps: int
    duration: int
    performance_score: Optional[float] = 0.0
    form_score: Optional[float] = 0.0
    consistency_score: Optional[float] = 0.0
    endurance_score: Optional[float] = 0.0
class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    date: str
    exercise: str
    reps: int
    duration: int
    performance_score: float
    form_score: float
    consistency_score: float
    endurance_score: float
    created_at: datetime
    class Config:
        from_attributes = True
# Habit Schemas
class HabitCreate(BaseModel):
    sleep_level: int = Field(..., ge=1, le=10)
    stress_level: int = Field(..., ge=1, le=10)
    days_inactive: int = Field(..., ge=1, le=7)
    workout_completed: Optional[bool] = False
    streak_days: Optional[int] = 0
class HabitResponse(BaseModel):
    id: int
    user_id: int
    date: str
    sleep_level: int
    stress_level: int
    days_inactive: int
    workout_completed: bool
    streak_days: int
    dropout_risk_score: float
    created_at: datetime
    class Config:
        from_attributes = True
# Diet Log Schemas
class DietLogCreate(BaseModel):
    food_items: str
    calories_consumed: int
    calories_target: int
    protein: Optional[int] = 0
    carbs: Optional[int] = 0
    fat: Optional[int] = 0
    date: Optional[str] = None
class DietLogResponse(BaseModel):
    id: int
    user_id: int
    date: str
    calories_consumed: int
    calories_target: int
    food_items: Optional[str]
    protein: int
    carbs: int
    fat: int
    created_at: datetime
    class Config:
        from_attributes = True
# Chat Schemas
class GymBuddyChatCreate(BaseModel):
    message: str
class GymBuddyChatResponse(BaseModel):
    id: int
    user_id: int
    sender: str
    message: str
    vibe: str
    created_at: datetime
    class Config:
        from_attributes = True
# Recommendation Schemas
class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    date: str
    type: str
    content: str
    created_at: datetime
    class Config:
        from_attributes = True
# Performance Score Schemas
class PerformanceScoreResponse(BaseModel):
    id: int
    user_id: int
    date: str
    performance_score: float
    form_score: float
    consistency_score: float
    endurance_score: float
    type: str
    created_at: datetime
    class Config:
        from_attributes = True
# Admin stats
class AdminStats(BaseModel):
    total_users: int
    active_users: int
    suspended_users: int
    total_workouts: int
    total_reps: int
    total_calories_logged: int