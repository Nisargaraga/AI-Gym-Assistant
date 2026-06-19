from .routers.auth import router as auth_router
from .routers.workout import router as workout_router
from .routers.diet import router as diet_router
from .routers.habits import router as habits_router
from .routers.chatbot import router as chatbot_router
from .routers.analytics import router as analytics_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from .database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Gym Assistant"
)

app.include_router(auth_router)
app.include_router(diet_router)
app.include_router(workout_router)
app.include_router(habits_router)
app.include_router(chatbot_router)
app.include_router(analytics_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
        "message": "AI Gym Assistant Running"
    }