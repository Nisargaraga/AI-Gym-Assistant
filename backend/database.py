import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Locate database in the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'gymfit.db')}"
# SQLAlchemy engine setup.
# 'connect_args={"check_same_thread": False}' is required only for SQLite to allow multiple threads.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Dependency to yield database session per request and close it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()