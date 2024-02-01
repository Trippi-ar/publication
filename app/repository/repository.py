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
        date=data.date,
        elevation=data.elevation,
        distance=data.distance,
        duration=data.duration,
        languages=data.languages,
        transport=data.transport,
        description=data.description,
        tools=data.tools,
        itinerary=data.itinerary,
        is_active=True,
        type=data.type,
    )
    db.add(activity)
    db.flush()
    db.commit()

    return activity


def get_activity_by_id(db: Session, activity_id: int):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise Exception("Activity not found")
    address = db.query(models.Address).filter(models.Address.id == activity.address_id).first()
    if address is None:
        raise Exception("Address not found")
    data = {
        "activity_id": activity.id,
        "name": activity.name,
        "difficulty": activity.difficulty,
        "address_id": activity.address_id,
        "tour_guide_id": activity.tour_guide_id,
        "created_at": activity.created_at,
        "updated_at": activity.updated_at,
        "date": activity.date,
        "elevation": activity.elevation,
        "distance": activity.distance,
        "duration": activity.duration,
        "price": activity.price,
        "languages": activity.languages,
        "transport": activity.transport,
        "description": activity.description,
        "tools": activity.tools,
        "itinerary": activity.itinerary,
        "is_active": activity.is_active,
        "type": activity.type,
        "lat": address.lat,
        "lng": address.lng,
        "country": address.country,
        "administrative_area_level_1": address.administrative_area_level_1,
        "administrative_area_level_2": address.administrative_area_level_2,
        "locality": address.locality,
        "postal_code": address.postal_code,
        "street": address.street,
        "street_number": address.street_number,
        "place_id": address.place_id,
        "address_created_at": address.created_at,
        "address_updated_at": address.updated_at,
        "address_is_active": address.is_active
    }
    return data


def get_activity_by_user_id(db: Session, user_id: int):
    activity = db.query(models.Activity).filter(models.Activity.tour_guide_id == user_id).all()
    if activity is None:
        raise Exception("Activity not found")
    data = []
    for i in activity:
        address = db.query(models.Address).filter(models.Address.id == i.address_id).first()
        if address is None:
            raise Exception("Address not found")
        data.append({
            "activity_id": i.id,
            "name": i.name,
            "difficulty": i.difficulty,
            "address_id": i.address_id,
            "tour_guide_id": i.tour_guide_id,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "date": i.date,
            "elevation": i.elevation,
            "distance": i.distance,
            "duration": i.duration,
            "price": i.price,
            "languages": i.languages,
            "transport": i.transport,
            "description": i.description,
            "tools": i.tools,
            "itinerary": i.itinerary,
            "is_active": i.is_active,
            "type": i.type,
            "lat": address.lat,
            "lng": address.lng,
            "country": address.country,
            "administrative_area_level_1": address.administrative_area_level_1,
            "administrative_area_level_2": address.administrative_area_level_2,
            "locality": address.locality,
            "postal_code": address.postal_code,
            "street": address.street,
            "street_number": address.street_number,
            "place_id": address.place_id,
            "address_created_at": address.created_at,
            "address_updated_at": address.updated_at,
            "address_is_active": address.is_active
        })

    return data


def get_activities(db: Session):
    activity = db.query(models.Activity).all()
    if activity is None:
        raise Exception("Activity not found")
    data = []
    for i in activity:
        address = db.query(models.Address).filter(models.Address.id == i.address_id).first()
        if address is None:
            raise Exception("Address not found")
        data.append({
            "activity_id": i.id,
            "name": i.name,
            "difficulty": i.difficulty,
            "address_id": i.address_id,
            "tour_guide_id": i.tour_guide_id,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "date": i.date,
            "elevation": i.elevation,
            "distance": i.distance,
            "duration": i.duration,
            "price": i.price,
            "languages": i.languages,
            "transport": i.transport,
            "description": i.description,
            "tools": i.tools,
            "itinerary": i.itinerary,
            "is_active": i.is_active,
            "type": i.type,
            "lat": address.lat,
            "lng": address.lng,
            "country": address.country,
            "administrative_area_level_1": address.administrative_area_level_1,
            "administrative_area_level_2": address.administrative_area_level_2,
            "locality": address.locality,
            "postal_code": address.postal_code,
            "street": address.street,
            "street_number": address.street_number,
            "place_id": address.place_id,
            "address_created_at": address.created_at,
            "address_updated_at": address.updated_at,
            "address_is_active": address.is_active
        })

    return data


def update_activity(db: Session, data: schema.ActivityUpdate):
    activity = db.query(models.Activity).filter(models.Activity.id == data.activity_id).first()
    if activity is None:
        raise Exception("Activity not found")

    address = db.query(models.Address).filter(models.Address.id == activity.address_id).first()
    if address is None:
        raise Exception("Address not found")

    activity.name = data.name
    activity.difficulty = data.difficulty
    activity.date = data.date
    activity.elevation = data.elevation
    activity.distance = data.distance
    activity.duration = data.duration
    activity.price = data.price
    activity.languages = data.languages
    activity.transport = data.transport
    activity.description = data.description
    activity.tools = data.tools
    activity.itinerary = data.itinerary
    activity.is_active = data.is_active
    activity.type = data.type
    db.commit()

    address.lat = data.lat
    address.lng = data.lng
    address.country = data.country
    address.administrative_area_level_1 = data.administrative_area_level_1
    address.administrative_area_level_2 = data.administrative_area_level_2
    address.locality = data.locality
    address.postal_code = data.postal_code
    address.street = data.street
    address.street_number = data.street_number
    address.place_id = data.place_id
    address.is_active = data.address_is_active
    address.updated_at = datetime.utcnow()
    db.commit()

    return activity


def get_activity_by_filters(db: Session, data: schema.ActivityFilter):
    activity = db.query(models.Activity).filter(
        models.Activity.name == data.name if data.name is not None else True,
        models.Activity.tour_guide_id == data.tour_guide_id if data.tour_guide_id is not None else True,
        models.Activity.difficulty == data.difficulty if data.difficulty is not None else True,
        models.Activity.distance == data.distance if data.distance is not None else True,
        models.Activity.date == data.date if data.date is not None else True,
        models.Activity.elevation == data.elevation if data.elevation is not None else True,
        models.Activity.duration == data.duration if data.duration is not None else True,
        models.Activity.price == data.price if data.price is not None else True,
        models.Activity.languages == data.languages if data.languages is not None else True,
        models.Activity.transport == data.transport if data.transport is not None else True,
        models.Activity.description == data.description if data.description is not None else True,
        models.Activity.tools == data.tools if data.tools is not None else True,
        models.Activity.itinerary == data.itinerary if data.itinerary is not None else True,
        models.Activity.type == data.type if data.type is not None else True,
        models.Activity.is_active == data.is_active if data.is_active is not None else True,
        models.Activity.created_at >= data.created_at if data.created_at is not None else True,
        models.Activity.created_at <= data.created_at if data.created_at is not None else True,
        models.Activity.updated_at >= data.updated_at if data.updated_at is not None else True,
        models.Activity.updated_at <= data.updated_at if data.updated_at is not None else True,
        models.Activity.date >= data.date if data.date is not None else True,
        models.Activity.date <= data.date if data.date is not None else True,
        models.Activity.elevation >= data.elevation if data.elevation is not None else True,
        models.Activity.elevation <= data.elevation if data.elevation is not None else True,
        models.Activity.distance >= data.distance if data.distance is not None else True,
        models.Activity.distance <= data.distance if data.distance is not None else True,
        models.Activity.duration >= data.duration if data.duration is not None else True,
        models.Activity.duration <= data.duration if data.duration is not None else True,
        models.Activity.price >= data.price if data.price is not None else True,
        models.Activity.price <= data.price if data.price is not None else True,
        models.Activity.is_active == data.is_active if data.is_active is not None else True,
        models.Activity.type == data.type if data.type is not None else True,
        models.Activity.created_at >= data.created_at if data.created_at is not None else True,
        models.Activity.created_at <= data.created_at if data.created_at is not None else True,
        models.Activity.updated_at >= data.updated_at if data.updated_at is not None else True,
        models.Activity.updated_at <= data.updated_at if data.updated_at is not None else True,
    ).all()
    if activity is None:
        raise Exception("Activity not found")
    data = []
    for i in activity:
        address = db.query(models.Address).filter(models.Address.id == i.address_id).first()
        if address is None:
            raise Exception("Address not found")
        data.append({
            "activity_id": i.id,
            "name": i.name,
            "difficulty": i.difficulty,
            "address_id": i.address_id,
            "tour_guide_id": i.tour_guide_id,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "date": i.date,
            "elevation": i.elevation,
            "distance": i.distance,
            "duration": i.duration,
            "price": i.price,
            "languages": i.languages,
            "transport": i.transport,
            "description": i.description,
            "tools": i.tools,
            "itinerary": i.itinerary,
            "is_active": i.is_active,
            "type": i.type,
            "lat": address.lat,
            "lng": address.lng,
            "country": address.country,
            "administrative_area_level_1": address.administrative_area_level_1,
            "administrative_area_level_2": address.administrative_area_level_2,
            "locality": address.locality,
            "postal_code": address.postal_code,
            "street": address.street,
            "street_number": address.street_number,
            "place_id": address.place_id,
            "address_created_at": address.created_at,
            "address_updated_at": address.updated_at,
            "address_is_active": address.is_active
        })
        return data


def get_activity_by_filters_paginated(db: Session, data: schema.ActivityFilter, page: int, size: int):
    activity = db.query(models.Activity).filter(
        models.Activity.name == data.name if data.name is not None else True,
        models.Activity.tour_guide_id == data.tour_guide_id if data.tour_guide_id is not None else True,
        models.Activity.difficulty == data.difficulty if data.difficulty is not None else True,
        models.Activity.distance == data.distance if data.distance is not None else True,
        models.Activity.date == data.date if data.date is not None else True,
        models.Activity.elevation == data.elevation if data.elevation is not None else True,
        models.Activity.duration == data.duration if data.duration is not None else True,
        models.Activity.price == data.price if data.price is not None else True,
        models.Activity.languages == data.languages if data.languages is not None else True,
        models.Activity.transport == data.transport if data.transport is not None else True,
        models.Activity.description == data.description if data.description is not None else True,
        models.Activity.tools == data.tools if data.tools is not None else True,
        models.Activity.itinerary == data.itinerary if data.itinerary is not None else True,
        models.Activity.type == data.type if data.type is not None else True,
        models.Activity.is_active == data.is_active if data.is_active is not None else True,
        models.Activity.created_at >= data.created_at if data.created_at is not None else True,
        models.Activity.created_at <= data.created_at if data.created_at is not None else True,
        models.Activity.updated_at >= data.updated_at if data.updated_at is not None else True,
        models.Activity.updated_at <= data.updated_at if data.updated_at is not None else True,
        models.Activity.date >= data.date if data.date is not None else True,
        models.Activity.date <= data.date if data.date is not None else True,
        models.Activity.elevation >= data.elevation if data.elevation is not None else True,
        models.Activity.elevation <= data.elevation if data.elevation is not None else True,
        models.Activity.distance >= data.distance if data.distance is not None else True,
        models.Activity.distance <= data.distance if data.distance is not None else True,
        models.Activity.duration >= data.duration if data.duration is not None else True,
        models.Activity.duration <= data.duration if data.duration is not None else True,
        models.Activity.price >= data.price if data.price is not None else True,
        models.Activity.price <= data.price if data.price is not None else True,
        models.Activity.is_active == data.is_active if data.is_active is not None else True,
        models.Activity.type == data.type if data.type is not None else True,
        models.Activity.created_at >= data.created_at if data.created_at is not None else True,
        models.Activity.created_at <= data.created_at if data.created_at is not None else True,
        models.Activity.updated_at >= data.updated_at if data.updated_at is not None else True,
        models.Activity.updated_at <= data.updated_at if data.updated_at is not None else True,
    ).offset(page).limit(size).all()
    if activity is None:
        raise Exception("Activity not found")
    data = []
    for i in activity:
        address = db.query(models.Address).filter(models.Address.id == i.address_id).first()
        if address is None:
            raise Exception("Address not found")
        data.append({
            "activity_id": i.id,
            "name": i.name,
            "difficulty": i.difficulty,
            "address_id": i.address_id,
            "tour_guide_id": i.tour_guide_id,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "date": i.date,
            "elevation": i.elevation,
            "distance": i.distance,
            "duration": i.duration,
            "price": i.price,
            "languages": i.languages,
            "transport": i.transport,
            "description": i.description,
            "tools": i.tools,
            "itinerary": i.itinerary,
            "is_active": i.is_active,
            "type": i.type,
            "lat": address.lat,
            "lng": address.lng,
            "country": address.country,
            "administrative_area_level_1": address.administrative_area_level_1,
            "administrative_area_level_2": address.administrative_area_level_2,
            "locality": address.locality,
            "postal_code": address.postal_code,
            "street": address.street,
            "street_number": address.street_number,
            "place_id": address.place_id,
            "address_created_at": address.created_at,
            "address_updated_at": address.updated_at,
            "address_is_active": address.is_active
        })
        return data


def delete_activity_by_id(db: Session, activity_id: int):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if activity is None:
        raise Exception("Activity not found")
    address = db.query(models.Address).filter(models.Address.id == activity.address_id).first()
    if address is None:
        raise Exception("Address not found")
    db.delete(activity)
    db.delete(address)
    db.commit()
    return {"message": "Activity deleted successfully"}


def delete_activity_by_user_id(db: Session, tour_guide_id: int):
    activity = db.query(models.Activity).filter(models.Activity.tour_guide_id == tour_guide_id).all()
    if activity is None:
        raise Exception("Activity not found")
    for i in activity:
        address = db.query(models.Address).filter(models.Address.id == i.address_id).first()
        if address is None:
            raise Exception("Address not found")
        db.delete(i)
        db.delete(address)
        db.commit()
    return {"message": "Activity deleted successfully"}


def create_booking(db: Session, data: schema.BookingCreate):
    if data.number_people <= 0:
        raise Exception("Number people must be greater than 0")

    activity = db.query(models.Activity).filter(models.Activity.id == data.activity_id).first()
    if activity is None:
        raise Exception("Activity not found")

    booking = models.Booking(
        activity_id=data.activity_id,
        user_id=data.user_id,
        date=data.date,
        number_people=data.number_people,
        price=data.price,
        state="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(booking)
    db.commit()

    return booking


def get_booking_by_id(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if booking is None:
        raise Exception("Booking not found")

    activity = db.query(models.Activity).filter(models.Activity.id == booking.activity_id).first()
    if activity is None:
        raise Exception("Activity not found")

    data = {
        "booking_id": booking.id,
        "activity_id": booking.activity_id,
        "user_id": booking.user_id,
        "date": booking.date,
        "number_people": booking.number_people,
        "price": booking.price,
        "state": booking.state,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
    }
    return data


def get_booking_by_user_id(db: Session, user_id: int):
    booking = db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
    if booking is None:
        raise Exception("Booking not found")
    data = []
    for i in booking:
        data.append({
            "booking_id": i.id,
            "activity_id": i.activity_id,
            "user_id": i.user_id,
            "date": i.date,
            "number_people": i.number_people,
            "price": i.price,
            "state": i.state,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
        })
    return data


def get_booking_by_activity_id(db: Session, activity_id: int):
    booking = db.query(models.Booking).filter(models.Booking.activity_id == activity_id).all()
    if booking is None:
        raise Exception("Booking not found")
    data = []
    for i in booking:
        data.append({
            "booking_id": i.id,
            "activity_id": i.activity_id,
            "user_id": i.user_id,
            "date": i.date,
            "number_people": i.number_people,
            "price": i.price,
            "state": i.state,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
        })
    return data


def update_booking(db: Session, data: schema.BookingUpdate):
    booking = db.query(models.Booking).filter(models.Booking.id == data.booking_id).first()
    if booking is None:
        raise Exception("Booking not found")

    booking.date = data.date
    booking.number_people = data.number_people
    booking.price = data.price
    booking.state = data.state
    booking.updated_at = datetime.utcnow()
    db.commit()
    return booking


def delete_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if booking is None:
        raise Exception("Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}


def delete_booking_by_user_id(db: Session, user_id: int):
    booking = db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
    if booking is None:
        raise Exception("Booking not found")
    for i in booking:
        db.delete(i)
        db.commit()
    return {"message": "Booking deleted successfully"}


def get_suggestions(db: Session, word: str):

    activity_names = db.query(models.Activity).filter(models.Activity.name.ilike(f'%{word}%')).limit(3).all()
    localities = db.query(models.Address).filter(models.Address.locality.ilike(f'%{word}%')).limit(3).all()
    if len(localities) < 3:
        remaining_limit = 3 - len(localities)
        area_levels = db.query(models.Address).filter(models.Address.administrative_area_level_1.ilike(f'%{word}%')).limit(remaining_limit).all()
    else:
        area_levels = []
    
    suggestions = schema.Suggestions(
        activities_name=[activity.name for activity in activity_names],
        address=[locality.locality for locality in localities] + [area_level.administrative_area_level_1 for area_level in area_levels]
    )

    return suggestions
