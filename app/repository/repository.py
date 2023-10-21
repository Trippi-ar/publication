from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from datetime import datetime

from app.db_config import database
from app.models import models
from app.schema import schema

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return models.Base.metadata.create_all(bind=database.engine)


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

