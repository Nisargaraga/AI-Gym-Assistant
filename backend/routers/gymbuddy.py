from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from auth import get_current_user
from services.gemini_service import GeminiService
import models
import schemas
router = APIRouter(prefix="/gymbuddy", tags=["Virtual Gym Buddy"])
@router.post("/", response_model=schemas.GymBuddyChatResponse)
async def chat_with_buddy(
    chat_in: schemas.GymBuddyChatCreate,
    api_key: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Store the user's message in the database
    user_chat = models.GymBuddyChat(
        user_id=current_user.id,
        sender="user",
        message=chat_in.message,
        vibe="supportive"
    )
    db.add(user_chat)
    db.commit()
    # 2. Retrieve recent chat history for context
    history = db.query(models.GymBuddyChat).filter(
        models.GymBuddyChat.user_id == current_user.id
    ).order_by(models.GymBuddyChat.created_at.asc()).limit(10).all()
    
    formatted_history = [
        {"sender": chat.sender, "message": chat.message}
        for chat in history
    ]
    # Calculate user streak from habits
    streak = 1
    recent_habit = db.query(models.HabitTracking).filter(
        models.HabitTracking.user_id == current_user.id
    ).order_by(models.HabitTracking.created_at.desc()).first()
    if recent_habit:
        streak = recent_habit.streak_days
    # 3. Call Gemini to generate a response
    user_profile = {
        "name": current_user.name,
        "goal": current_user.goal
    }
    
    reply_text, vibe = await GeminiService.generate_buddy_chat(
        message=chat_in.message,
        user_profile=user_profile,
        chat_history=formatted_history[:-1], # exclude current unsaved bot reply
        streak=streak,
        api_key=api_key
    )
    # 4. Store the bot's response in the database
    bot_chat = models.GymBuddyChat(
        user_id=current_user.id,
        sender="bot",
        message=reply_text,
        vibe=vibe
    )
    db.add(bot_chat)
    db.commit()
    db.refresh(bot_chat)
    return bot_chat
@router.get("/history", response_model=List[schemas.GymBuddyChatResponse])
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Returns last 30 messages
    return db.query(models.GymBuddyChat).filter(
        models.GymBuddyChat.user_id == current_user.id
    ).order_by(models.GymBuddyChat.created_at.asc()).limit(30).all()