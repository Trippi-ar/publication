from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import List

from app.schema import booking_schema
from app.service.booking_service import BookingService

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/booking",
    tags=['Booking']
)


@router.post("/", status_code=status.HTTP_200_OK, response_model=booking_schema.Response)
def create_booking(
        booking: booking_schema.Request,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        booking_service: BookingService = Depends(BookingService),
):
    """
    Create a booking
    """
    return booking_service.create(booking, token)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[booking_schema.Response])
def get_bookings(
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        booking_service: BookingService = Depends(BookingService),
):
    """
    Get bookings for a user
    """
    return booking_service.get_all(token)


@router.post("/availability", status_code=status.HTTP_200_OK, response_model=bool)
def check_availability(
        availability: booking_schema.Availability,
        booking_service: BookingService = Depends(BookingService),
):
    """
    Check availability for a publication
    """
    return booking_service.check_availability(availability)
