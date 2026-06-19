from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)
    password = Column(String)

    name = Column(String)

    weight = Column(Float)
    height = Column(Float)

    goal = Column(String)
    diet_preference = Column(String)


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    exercise = Column(String)

    reps = Column(Integer)

    accuracy = Column(Float)


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    streak = Column(Integer)

    missed_days = Column(Integer)

    prediction = Column(String)