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


def create_activity(db: Session, data: schema.ActivityCreate):
    address = models.Address(
        country=data.country,
        administrative_area_level_1=data.administrative_area_level_1,
        locality=data.locality,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(address)
    db.flush()

    activity = models.Activity(
        name=data.name,
        difficulty=data.difficulty,
        tour_guide_id=data.tour_guide_id,
        address_id=address.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        likes = 0,
        date = data.date,
        desnivel = data.desnivel,
        distance = data.distance,
        price = data.price,
    )
    db.add(activity)
    db.flush()

    activity_details = models.ActivityDetails(
        type = data.type,
        requirements = data.requirements,
        information = data.information,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
        activity_id = activity.id
    )

    db.add(activity_details)

    db.commit()
