from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.repository import repository
from app.schema import schema
from app.utils import utils

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/booking",
    tags=['Booking']
)


@router.post("/", status_code=status.HTTP_200_OK)
def create_booking(
        booking_create: schema.BookingCreate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Crea una nueva reserva.
    """
    utils.authenticate_and_authorize(token.credentials, "user")
    booking_create.user_id = authenticate_and_authorize.get("user_id")
    response = repository.create_booking(db, booking_create)

    return response


@router.get("/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(
        booking_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene los detalles de una reserva por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "user")
    response = repository.get_booking_by_id(db, booking_id)

    return response


@router.get("/", status_code=status.HTTP_200_OK)
def get_booking_by_user_id(
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene las reservas de un usuario por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "user")
    response = repository.get_booking_by_user_id(db, authenticate_and_authorize.get("user_id"))

    return response


@router.get("/activity_booking/{activity_id}", status_code=status.HTTP_200_OK)
def get_booking_by_activity_id(
        activity_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Obtiene las reservas de una actividad por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "guide")
    response = repository.get_booking_by_activity_id(db, activity_id)
    
    return response


@router.put("/", status_code=status.HTTP_200_OK)
def update_booking(
        booking_create: schema.BookingUpdate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Actualiza una reserva.
    """
    utils.authenticate_and_authorize(token.credentials, "user")
    booking_create.user_id = authenticate_and_authorize.get("user_id")
    response = repository.update_booking(db, booking_create)

    return response


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_booking(
        booking_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
    ):
    """
    Elimina una reserva por su ID.
    """
    utils.authenticate_and_authorize(token.credentials, "user")
    response = repository.delete_booking(db, booking_id)
    
    return response
