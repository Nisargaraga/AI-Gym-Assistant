import numpy as np
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sklearn.linear_model import LogisticRegression
from database import get_db
from auth import get_current_user
import models
import schemas
router = APIRouter(prefix="/habits", tags=["Habits & Dropout Prediction"])
# Instantiate and fit a global Logistic Regression model on startup
# Features: [days_inactive, sleep_level, stress_level]
# Output: Probability of dropout (skipping next workout)
predictor_model = LogisticRegression()
def train_predictor_model():
    """
    Train a Logistic Regression model on a synthetic dataset reflecting fitness behaviors:
    - High inactive days + high stress + low sleep = High risk of skipping (1)
    - Low inactive days + good sleep + low stress = Low risk of skipping (0)
    """
    np.random.seed(42)
    X = []
    y = []
    # Generate synthetic training examples
    for _ in range(250):
        days_inactive = np.random.randint(1, 8)  # 1 to 7 days
        sleep = np.random.randint(3, 11)         # 3 to 10 hours
        stress = np.random.randint(1, 11)        # 1 to 10 level
        
        # Calculate risk logic:
        # If days inactive is high, and sleep is low, and stress is high -> high probability of skipping
        score = (days_inactive * 1.5) - (sleep * 0.8) + (stress * 0.5)
        
        # Logistic sigmoid probability approximation
        prob = 1 / (1 + np.exp(-score))
        label = 1 if prob > 0.5 else 0
        
        X.append([days_inactive, sleep, stress])
        y.append(label)
    predictor_model.fit(np.array(X), np.array(y))
    print("AI Habit Risk Model successfully trained with Scikit-learn.")
# Train the model upon module import
train_predictor_model()
@router.post("/", response_model=schemas.HabitResponse)
def log_habit(
    habit_in: schemas.HabitCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    day_str = datetime.now().strftime("%a")
    # Use the Scikit-learn model to predict the probability of skipping the next workout
    # Input format: [days_inactive, sleep_level, stress_level]
    features = np.array([[habit_in.days_inactive, habit_in.sleep_level, habit_in.stress_level]])
    
    # predict_proba returns [prob_class_0, prob_class_1]
    probabilities = predictor_model.predict_proba(features)
    skip_risk_probability = float(probabilities[0][1])  # probability of class 1 (skipping)
    
    # Convert to percentage
    risk_percentage = round(skip_risk_probability * 100.0, 1)
    # Check if a log already exists for today
    existing = db.query(models.HabitTracking).filter(
        models.HabitTracking.user_id == current_user.id,
        models.HabitTracking.date == day_str
    ).first()
    if existing:
        existing.sleep_level = habit_in.sleep_level
        existing.stress_level = habit_in.stress_level
        existing.days_inactive = habit_in.days_inactive
        existing.workout_completed = habit_in.workout_completed or existing.workout_completed
        existing.streak_days = habit_in.streak_days or existing.streak_days
        existing.dropout_risk_score = risk_percentage
        db.commit()
        db.refresh(existing)
        return existing
    # Create new habit tracker log
    habit = models.HabitTracking(
        user_id=current_user.id,
        date=day_str,
        sleep_level=habit_in.sleep_level,
        stress_level=habit_in.stress_level,
        days_inactive=habit_in.days_inactive,
        workout_completed=habit_in.workout_completed,
        streak_days=habit_in.streak_days,
        dropout_risk_score=risk_percentage
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit
@router.get("/", response_model=List[schemas.HabitResponse])
def get_habit_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.HabitTracking).filter(
        models.HabitTracking.user_id == current_user.id
    ).order_by(models.HabitTracking.created_at.desc()).all()