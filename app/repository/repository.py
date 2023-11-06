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


def update_activity(db: Session, data: schema.ActivityUpdate):
    activity = db.query(models.Activity).filter(models.Activity.id == data.id).first()
    if activity:
        if data.tour_guide_id == activity.tour_guide_id:
            activity.difficulty = data.difficulty or activity.difficulty
            activity.date = data.date or activity.date
            activity.elevation = data.elevation or activity.elevation
            activity.distance = data.distance or activity.distance
            activity.price = data.price or activity.price
            db.commit()
            db.flush()
            activitydetails = db.query(models.ActivityDetails).filter(models.ActivityDetails.activity_id == data.id).first()
            activitydetails.type = data.type or activitydetails.type
            activitydetails.requirements =data.requirements or activitydetails.requirements
            activitydetails.information = data.information or activitydetails.information
            db.commit()
        else:
           return {"message": "User does not own this activity"}
    else:
        return {"message": "activity not found"}


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
    activity = db.query(models.Activity).filter(models.Activity.tour_guide_id == tour_guide_id).first()
    if activity is None:
        return None
    activitydetails = db.query(models.ActivityDetails).filter(models.ActivityDetails.activity_id == activity.id).first()
    if activitydetails is None:
        return None
    activitylikes = like_count = db.query(func.count(models.Likes.id)).filter(
        models.Likes.activity == activity.id).scalar()
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



def get_activities(db: Session):
    activities = db.query(models.Activity).all()
    response = schema.MultiplesActivities()
    response.activities = []

    for activity in activities:
        activity_details = db.query(models.ActivityDetails).filter_by(activity_id=activity.id).first()

        if activity_details:
            activity_with_details = schema.ActivityWithDetails(
                activity_id=activity.id,
                name=activity.name,
                tour_guide_id=activity.tour_guide_id,
                difficulty=activity.difficulty,
                distance=activity.distance,
                date=activity.date,
                elevation=activity.elevation,
                price=activity.price,
                details=schema.ActivityDetails(
                    type=activity_details.type,
                    requirements=activity_details.requirements,
                    information=activity_details.information,
                )
            )
            response.activities.append(activity_with_details)

    return response


def delete_activity(db: Session, data: schema.DeleteActivity):

    activity = db.query(models.Activity).filter(models.Activity.id == data.activity_id).first()
    if activity:
        if data.user_id == activity.tour_guide_id:
            db.delete(activity)
            db.commit()
        else:
            return {"message":"User does not own this activity"}
        return {"message": "Activity deleted successfully"}
    else:
        return {"message": "Activity not found"}
