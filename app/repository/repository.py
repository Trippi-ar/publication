from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
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
        date=data.date,
        elevation=data.elevation,
        distance=data.distance,
        price=data.price,
    )
    db.add(activity)
    db.flush()

    activity_details = models.ActivityDetails(
        type=data.type,
        requirements=data.requirements,
        information=data.information,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        activity_id=activity.id
    )

    db.add(activity_details)

    db.commit()


def get_activity_by_id(db: Session, activity_id: int):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        return None
    activitydetails = db.query(models.ActivityDetails).filter(models.ActivityDetails.activity_id == activity_id).first()
    if activitydetails is None:
        return None
    activitylikes = like_count = db.query(func.count(models.Likes.id)).filter(models.Likes.activity == activity_id).scalar()
    data = {"activity_id": activity.id,
            "name": activity.name,
            "tour_guide_id": activity.tour_guide_id,
            "likes": activitylikes,
            "difficulty": activity.difficulty,
            "distance": activity.distance,
            "date": activity.date,
            "elevation": activity.elevation,
            "price": activity.price,
            "type": activitydetails.type,
            "requirements": activitydetails.requirements,
            "information": activitydetails.information,
            }
    return data

def get_activity_by_guide_id(db: Session, tour_guide_id: str):
    return db.query(models.Activity).filter(models.Activity.tour_guide_id == tour_guide_id).first()


def get_activities(db: Session, tour_guide_id: str):
    return db.query(models.Activity).all()


def like_activity(db: Session, data: schema.LikeActivity):
        likes = db.query(models.Likes).filter(models.Likes.activity == data.activity_id ).filter(models.Likes.user_id == data.user_id).first()
        if likes is None:
            like = models.Likes(
                activity = data.activity_id,
                user_id = data.user_id,
                created_at = datetime.utcnow(),
                updated_at = datetime.utcnow()
            )

            db.flush()
            db.add(like)

            db.commit()


