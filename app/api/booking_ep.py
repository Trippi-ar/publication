from fastapi import Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/booking",
    tags=['Booking']
)


@router.post("/", status_code=status.HTTP_200_OK)
def create_booking():
    pass
