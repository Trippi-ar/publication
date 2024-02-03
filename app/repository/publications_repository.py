from sqlalchemy.exc import SQLAlchemyError

from contextlib import contextmanager

from app.db_config import database
from app.models import models
from app.schema import publication_schema
from app.utils import errors


def _add_tables():
    return models.Base.metadata.create_all(bind=database.engine)


class PublicationRepository:
    @staticmethod
    @contextmanager
    def _get_db_session():
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def create(data: publication_schema.Create):
        with PublicationRepository._get_db_session() as db:
            try:
                new_address = models.Address(
                    country=data.country,
                    administrative_area_level_1=data.administrative_area_level_1,
                    locality=data.locality,
                    full_address=f"{data.locality}, {data.administrative_area_level_1}, {data.country}",
                )
                db.add(new_address)
                # db.flush()
                new_publication = models.Publication(
                    address_id=new_address.id,
                    tour_guide_id=data.tour_guide_id,
                    name=data.name,
                    difficulty=data.difficulty,
                    distance=data.distance,
                    duration=data.duration,
                    price=data.price,
                    description=data.description,
                    tools=data.tools,
                    type=data.type,
                )
                db.add(new_publication)
                # db.flush()
                new_activities = [
                    models.Activity(
                        publication_id=new_publication.id,
                        date=date,
                        max_participants=data.max_participants,
                        available_spots=data.max_participants
                    ) for date in data.dates
                ]
                db.add_all(new_activities)
                new_languages = [
                    models.Languages(
                        publication_id=new_publication.id,
                        language=language
                    ) for language_string in data.languages
                    for language in language_string.split(',')
                ]
                db.add_all(new_languages)
                new_images = [
                    models.Images(
                        publication_id=new_publication.id,
                        image_url=image
                    ) for image in data.images
                ]
                db.add_all(new_images)
                db.flush()
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                error_message = str(e.orig)
                if "duplicate key value violates unique constraint" in error_message and "publication_name_key" in error_message:
                    raise errors.DuplicatePublicationNameError("Publication name already exists")
                if "invalid input value for enum" in error_message:
                    raise errors.InvalidInputError("Invalid input")
                else:
                    raise errors.RepositoryError(e)
