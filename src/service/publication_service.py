import uuid

from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from src.utils.utils import authenticate
from src.utils import errors
from src.repository.publications_repository import PublicationRepository
from src.schema import publication_schema
from src.config import configure_firebase


class PublicationService:
    @staticmethod
    def create(request, token, images_file_names):
        try:
            authentication = authenticate(token.credentials, 'guide')
            publication = publication_schema.Create(
                tour_guide_id=authentication.get('user_id'),
                name=request.name,
                difficulty=request.difficulty,
                distance=request.distance,
                duration=request.duration,
                price=request.price,
                description=request.description,
                tools=request.tools,
                type=request.type,
                languages=request.languages,
                max_participants=request.max_participants,
                dates=request.dates,
                images=images_file_names,
                country=request.country,
                administrative_area_level_1=request.administrative_area_level_1,
                locality=request.locality
            )
            repository = PublicationRepository()
            return repository.create(publication)

        except errors.AuthenticationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        except errors.DuplicatePublicationNameError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Publication name already exists")

        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

        except errors.InvalidInputError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

        except Exception:
            raise Exception

    @staticmethod
    async def upload_image(images):
        try:
            image_file_names = []
            for image in images:
                if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image format not supported")
            firebase = configure_firebase()
            storage = firebase.storage()
            for image in images:
                images_uuid = uuid.uuid4()
                image_name = f"{images_uuid}.{image.content_type.split('/')[1]}"
                new_image = await image.read()
                storage.child(image_name).put(new_image, content_type=image.content_type)
                image_url = storage.child(image_name).get_url(token=None)
                image_file_names.append(image_url)
            return image_file_names
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image upload failed")

    @staticmethod
    def get(publication_id):
        try:
            repository = PublicationRepository()
            return repository.get(publication_schema.Params(id=publication_id))
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Publication retrieval failed")

    @staticmethod
    def get_all(pagination, _filter):
        try:
            repository = PublicationRepository()
            return repository.get_all(pagination, _filter)
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Publications retrieval failed")

    @staticmethod
    def get_suggestions(suggestion):
        try:
            repository = PublicationRepository()
            return repository.get_suggestions(suggestion)
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Suggestions retrieval failed")

    @staticmethod
    def search(pagination: publication_schema.Pagination, search_filter: publication_schema.SearchFilter):
        try:
            repository = PublicationRepository()
            return repository.search(pagination, search_filter)
        except errors.RepositoryError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Search failed")
