from sqlalchemy.exc import SQLAlchemyError

from contextlib import contextmanager

from app.db_config import database
from app.models import models
from app.schema import booking_schema
from app.utils import errors


def _add_tables():
    return models.Base.metadata.create_all(bind=database.engine)


class BookingRepository:
    @staticmethod
    @contextmanager
    def _get_db_session():
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def create(create_booking: booking_schema.Create):
        with BookingRepository._get_db_session() as db:
            try:
                activity = db.query(models.Activity).filter(
                    models.Activity.publication_id == create_booking.publication_id).first()
                if activity is None:
                    raise errors.RepositoryError("Activity not found")
                activity.available_spots -= create_booking.participant
                available_spots = activity.available_spots
                if available_spots < 0:
                    raise errors.RepositoryError("Not enough spots available")
                publication = db.query(models.Publication).filter(
                    models.Publication.id == create_booking.publication_id).first()
                booking = models.Booking(
                    activity_id=activity.id,
                    user_id=create_booking.user_id,
                    quantity=create_booking.participant,
                    date=create_booking.date,
                    price=publication.price * create_booking.participant,
                    state="pending"
                )
                db.add(booking)
                db.commit()
                return booking_schema.Response(
                    id=booking.id,
                    name=publication.name,
                    user_id=booking.user_id,
                    date=booking.date,
                    participant=booking.quantity,
                    price=booking.price,
                    state=booking.state,
                    created_at=booking.created_at
                )
            except SQLAlchemyError as e:
                db.rollback()
                raise errors.RepositoryError(e)

    @staticmethod
    def get_all(user_id):
        with BookingRepository._get_db_session() as db:
            try:
                bookings = db.query(models.Booking).filter(
                    models.Booking.user_id == user_id).all()
                response = []
                for booking in bookings:
                    publication = db.query(models.Publication).filter(
                        models.Publication.id == booking.activity.publication_id).first()
                    response.append(booking_schema.Response(
                        id=booking.id,
                        name=publication.name,
                        user_id=booking.user_id,
                        date=booking.date,
                        participant=booking.quantity,
                        price=booking.price,
                        state=booking.state,
                        created_at=booking.created_at,
                    ))
                return response
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)

    @staticmethod
    def check_availability(availability: booking_schema.Availability):
        with BookingRepository._get_db_session() as db:
            try:
                publication = db.query(models.Publication).filter(
                    models.Publication.id == availability.publication_id).first()
                if publication is None:
                    raise errors.RepositoryError("Publication not found")
                activity = db.query(models.Activity).filter(
                    models.Activity.publication_id == availability.publication_id).filter(
                    models.Activity.date == availability.date).first()
                if activity is None:
                    return False
                if activity.available_spots < availability.participant:
                    return False
                return True
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)
