from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import config

engine = create_engine(config.DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
