from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
# Import local backend files
from database import engine, Base, get_db
import models
import schemas
import auth
# Import routers
from routers import workouts, dietician, gymbuddy, habits, analytics
# Create database tables automatically
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="AI Gym & Fitness Assistant API",
    description="Unified API endpoints for fitness tracking, dietician suggestions, habit predictors, and buddy companion chatbots.",
    version="1.0.0"
)
# CORS Configuration
# Allow local requests from frontend browser apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify front-end domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount Modular Routers
app.include_router(workouts.router)
app.include_router(dietician.router)
app.include_router(gymbuddy.router)
app.include_router(habits.router)
app.include_router(analytics.router)
# --- AUTHENTICATION & PROFILE ENDPOINTS ---
@app.post("/auth/register", response_model=schemas.UserResponse, tags=["Authentication"])
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if this is the first user, make them admin
    total_users = db.query(models.User).count()
    is_admin = True if total_users == 0 else False
    hashed_pw = auth.get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        hashed_password=hashed_pw,
        name=user_in.name,
        weight=user_in.weight,
        height=user_in.height,
        goal=user_in.goal,
        diet_preference=user_in.diet_preference,
        status="Active",
        is_admin=is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.post("/auth/login", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status == "Suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your profile is suspended. Please check console."
        )
    access_token_expires = timedelta(days=auth.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/auth/profile", response_model=schemas.UserResponse, tags=["Authentication"])
def get_user_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
@app.put("/auth/profile", response_model=schemas.UserResponse, tags=["Authentication"])
def update_user_profile(
    profile_in: schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    current_user.name = profile_in.name
    current_user.weight = profile_in.weight
    current_user.height = profile_in.height
    current_user.goal = profile_in.goal
    current_user.diet_preference = profile_in.diet_preference
    db.commit()
    db.refresh(current_user)
    return current_user
# --- ADMINISTRATIVE ENDPOINTS ---
@app.get("/admin/stats", response_model=schemas.AdminStats, tags=["Administration"])
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_admin_user)
):
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.status == "Active").count()
    suspended_users = db.query(models.User).filter(models.User.status == "Suspended").count()
    total_workouts = db.query(models.WorkoutHistory).count()
    
    # Calculate sum of reps
    reps_result = db.query(models.WorkoutHistory.reps).all()
    total_reps = sum(r[0] for r in reps_result) if reps_result else 0
    # Calculate calories
    cals_result = db.query(models.DietLog.calories_consumed).all()
    total_cals = sum(c[0] for c in cals_result) if cals_result else 0
    return {
        "total_users": total_users,
        "active_users": active_users,
        "suspended_users": suspended_users,
        "total_workouts": total_workouts,
        "total_reps": total_reps,
        "total_calories_logged": total_cals
    }
@app.get("/admin/users", response_model=List[schemas.UserResponse], tags=["Administration"])
def admin_list_users(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_admin_user)
):
    return db.query(models.User).all()
@app.put("/admin/users/{user_id}", response_model=schemas.UserResponse, tags=["Administration"])
def admin_update_user(
    user_id: int,
    user_update: schemas.AdminUserUpdate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_id == admin_user.id and user_update.status == "Suspended":
        raise HTTPException(status_code=400, detail="Admins cannot suspend their own active account session")
    user.status = user_update.status
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin
        
    db.commit()
    db.refresh(user)
    return user
@app.delete("/admin/users/{user_id}", tags=["Administration"])
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_admin_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_id == admin_user.id:
        raise HTTPException(status_code=400, detail="Admins cannot remove their own active profile")
    db.delete(user)
    db.commit()
    return {"detail": "User account and all related history successfully removed"}
@app.get("/", tags=["General"])
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the AI Gym & Fitness Assistant API ecosystem. Access documentation at /docs"
    }