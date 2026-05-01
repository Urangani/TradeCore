from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import DB_URL

engine_kwargs = {"pool_pre_ping": True}
if DB_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DB_URL, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
