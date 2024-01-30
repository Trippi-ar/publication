from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.repository import repository
from app.schema import schema
from app.utils import utils

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api",
    tags=['Activity']
)


@router.post("/", status_code=status.HTTP_200_OK)
def create_activity(
        activity_create: schema.ActivityCreate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
        ):
        """
        Crea una nueva actividad.
        """
        utils.authenticate_and_authorize(token.credentials, "guide")
        activity_create.tour_guide_id = authenticate.get("user_id")
        response = repository.create_activity(db, activity_create)

        return response


@router.get("/{activity_id}/", status_code=status.HTTP_200_OK)
def get_activity_by_id(
        activity_id: int, 
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene los detalles de una actividad por su ID.
    """
    response = repository.get_activity_by_id(db, activity_id)

    return response


@router.get("/user_activity/{user_id}", status_code=status.HTTP_200_OK)
def get_activity(
        user_id: int,
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene las actividades de un usuario por su ID.
    """
    response = repository.get_activity_by_user_id(db, user_id)

    return response


@router.get("/activities/", status_code=status.HTTP_200_OK)
def get_activities(
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene todas las actividades.
    """
    response = repository.get_activities(db)

    return response


@router.put("/", status_code=status.HTTP_200_OK)
def update_activity(
        activity_create: schema.ActivityUpdate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Actualiza una actividad.
    """
    utils.authenticate_and_authorize(token.credentials, "guide")
    activity_create.tour_guide_id = authenticate_and_authorize.get("user_id")
    response = repository.update_activity(db, activity_create)

    return response


@router.delete("/{activity_id}/", status_code=status.HTTP_200_OK)
def delete_activity(
        activity_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Elimina una actividad por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "guide")
    response = repository.delete_activity_by_id(db, activity_id)

    return response


@router.get("/activity_by_filters/", status_code=status.HTTP_200_OK)
def get_activity_by_filters(
        activity_filter: schema.ActivityFilter,
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene actividades filtradas por criterios específicos.
    """
    activities = repository.get_activity_by_filters(db, activity_filter)

    return activities


@router.delete("/activity_by_tour_guide/", status_code=status.HTTP_200_OK)
def delete_activity_by_user_id(
        tour_guide_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Elimina todas las actividades asociadas a un guía turístico por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "guide")
    response = repository.delete_activity_by_user_id(db, tour_guide_id)

    return response



