from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    weight = Column(Float, default=70.0)
    height = Column(Float, default=170.0)
    goal = Column(String, default="maintain")  # lean, bulk, maintain
    diet_preference = Column(String, default="balanced")  # balanced, vegan, keto, vegetarian
    status = Column(String, default="Active")  # Active, Suspended
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    workouts = relationship("WorkoutHistory", back_populates="user", cascade="all, delete-orphan")
    habits = relationship("HabitTracking", back_populates="user", cascade="all, delete-orphan")
    diet_logs = relationship("DietLog", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    performance_scores = relationship("PerformanceScore", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("GymBuddyChat", back_populates="user", cascade="all, delete-orphan")
class WorkoutHistory(Base):
    __tablename__ = "workout_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)  # "Mon", "Tue" or date string
    exercise = Column(String, nullable=False)  # squat, curl, pushup
    reps = Column(Integer, default=0)
    duration = Column(Integer, default=0)  # minutes
    performance_score = Column(Float, default=0.0)
    form_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    endurance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="workouts")
class HabitTracking(Base):
    __tablename__ = "habit_tracking"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    sleep_level = Column(Integer, default=7)  # 1-10
    stress_level = Column(Integer, default=5)  # 1-10
    days_inactive = Column(Integer, default=1)
    workout_completed = Column(Boolean, default=False)
    streak_days = Column(Integer, default=0)
    dropout_risk_score = Column(Float, default=0.0)  # risk probability
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="habits")
class DietLog(Base):
    __tablename__ = "diet_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    calories_consumed = Column(Integer, default=0)
    calories_target = Column(Integer, default=2000)
    food_items = Column(String, nullable=True)  # comma separated list or description
    protein = Column(Integer, default=0)  # grams
    carbs = Column(Integer, default=0)  # grams
    fat = Column(Integer, default=0)  # grams
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="diet_logs")
class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    type = Column(String, nullable=False)  # diet, workout, gym
    content = Column(String, nullable=False)  # JSON or text containing recommendations
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recommendations")
class PerformanceScore(Base):
    __tablename__ = "performance_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    performance_score = Column(Float, default=0.0)
    form_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    endurance_score = Column(Float, default=0.0)
    type = Column(String, default="weekly")  # weekly or monthly
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="performance_scores")
class GymBuddyChat(Base):
    __tablename__ = "gym_buddy_chats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String, nullable=False)  # user, bot
    message = Column(String, nullable=False)
    vibe = Column(String, default="supportive")  # supportive, hyped, empathetic
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="chats")