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
                db.flush()
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
                db.flush()

                new_activities = [
                    models.Activity(
                        publication_id=new_publication.id,
                        date=date,
                        max_participants=data.max_participants,
                        available_spots=data.max_participants
                    ) for date_string in data.dates
                    for date in date_string.split(',')
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
                return str(new_publication.id)
            except SQLAlchemyError as e:
                db.rollback()
                error_message = str(e.orig)
                if "duplicate key value violates unique constraint" in error_message and "publication_name_key" in error_message:
                    raise errors.DuplicatePublicationNameError("Publication name already exists")
                if "invalid input value for enum" in error_message:
                    raise errors.InvalidInputError("Invalid input")
                else:
                    raise errors.RepositoryError(e)

    @staticmethod
    def get(params: publication_schema.Params):
        with PublicationRepository._get_db_session() as db:
            try:
                publication = None
                if params.id is not None:
                    publication = db.query(models.Publication).filter(models.Publication.id == params.id).first()
                elif params.name is not None:
                    publication = db.query(models.Publication).filter(models.Publication.name == params.name).first()
                if publication is None:
                    raise errors.RepositoryError("Publication not found")
                address = db.query(models.Address).filter(models.Address.id == publication.address_id).first()
                languages = db.query(models.Languages).filter(models.Languages.publication_id == publication.id).all()
                activities = db.query(models.Activity).filter(models.Activity.publication_id == publication.id).all()
                images = db.query(models.Images).filter(models.Images.publication_id == publication.id).all()
                publication = publication_schema.GetResponse(
                    id=str(publication.id),
                    name=publication.name,
                    difficulty=publication.difficulty,
                    distance=publication.distance,
                    duration=publication.duration,
                    price=publication.price,
                    description=publication.description,
                    tools=publication.tools,
                    type=publication.type,
                    languages=[language.language for language in languages],
                    max_participants=activities[0].max_participants,
                    dates=[str(activity.date) for activity in activities],
                    images=[image.image_url for image in images],
                    country=address.country,
                    administrative_area_level_1=address.administrative_area_level_1,
                    locality=address.locality,
                    full_address=address.full_address
                )
                return publication
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)

    @staticmethod
    def get_all(pagination: publication_schema.Pagination, filters: publication_schema.Filter):
        with PublicationRepository._get_db_session() as db:
            try:
                query = db.query(models.Publication)
                if filters.name is not None:
                    query = query.filter(models.Publication.name == filters.name)
                elif filters.difficulty is not None:
                    query = query.filter(models.Publication.difficulty == filters.difficulty)
                elif filters.max_price is not None:
                    query = query.filter(models.Publication.price <= filters.max_price)
                elif filters.min_price is not None:
                    query = query.filter(models.Publication.price >= filters.min_price)
                elif filters.max_duration is not None:
                    query = query.filter(models.Publication.duration <= filters.max_duration)
                elif filters.min_duration is not None:
                    query = query.filter(models.Publication.duration >= filters.min_duration)
                elif filters.max_distance is not None:
                    query = query.filter(models.Publication.distance <= filters.max_distance)
                elif filters.min_distance is not None:
                    query = query.filter(models.Publication.distance >= filters.min_distance)
                elif filters.type is not None:
                    query = query.filter(models.Publication.type == filters.type)
                elif filters.languages is not None:
                    query = query.join(models.Languages).filter(models.Languages.language == filters.languages)
                elif filters.locality is not None:
                    query = query.join(models.Address).filter(models.Address.locality == filters.locality)
                elif filters.administrative_area_level_1 is not None:
                    query = query.join(models.Address).filter(
                        models.Address.administrative_area_level_1 == filters.administrative_area_level_1)
                elif filters.country is not None:
                    query = query.join(models.Address).filter(models.Address.country == filters.country)
                elif filters.available_spots is not None:
                    query = query.join(models.Activity).filter(models.Activity.available_spots >= filters.available_spots)
                if query is None:
                    raise errors.RepositoryError("No publications found")
                publications = query.limit(pagination.per_page).offset(
                    (pagination.page - 1) * pagination.per_page).all()
                publications = [PublicationRepository.get(publication_schema.Params(id=publication.id)) for publication
                                in publications]
                return publications
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)

    @staticmethod
    def get_suggestions(keyword: str):
        with PublicationRepository._get_db_session() as db:
            try:
                full_address_results = db.query(models.Address).filter(
                    models.Address.full_address.like(f'%{keyword}%')).limit(5).all()
                publication_name_results = db.query(models.Publication).filter(
                    models.Publication.name.like(f'%{keyword}%')).limit(5).all()
                return publication_schema.Suggestions(
                    name=[publication.name for publication in publication_name_results],
                    full_address=[address.full_address for address in full_address_results]
                )
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)

    @staticmethod
    def search(pagination: publication_schema.Pagination, word: str):
        with PublicationRepository._get_db_session() as db:
            try:
                query = db.query(models.Publication)
                query = query.filter(models.Publication.name.like(f'%{word}%'))
                query = query.join(models.Address).filter(models.Address.full_address.like(f'%{word}%'))
                if query is None:
                    raise errors.RepositoryError("No publications found")
                publications = query.limit(pagination.per_page).offset(
                    (pagination.page - 1) * pagination.per_page).all()
                publications = [PublicationRepository.get(publication_schema.Params(id=publication.id)) for publication
                                in publications]
                return publications
            except SQLAlchemyError as e:
                raise errors.RepositoryError(e)
