from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import Settings
from src.models.models import Base


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_engine(Settings.DATABASE_URI)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



