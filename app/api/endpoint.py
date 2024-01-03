from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.repository import repository

from app.schema import schema
from app.auth import auth

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/activity",
    tags=['Activity']
)


@router.post("/", status_code=status.HTTP_200_OK)
def create_activity(
        activity_create: schema.ActivityCreate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    activity_create.tour_guide_id = authenticate.get("user_id")
    activity_created = repository.create_activity(db, activity_create)

    return activity_created


@router.get("/get_activity_by_id/", status_code=status.HTTP_200_OK)
def get_activity(
        activity_id: int,
        db: Session = Depends(repository.get_db)
):
    activity = repository.get_activity_by_id(db, activity_id)
    return activity


@router.get("/get_activity_by_user_id/", status_code=status.HTTP_200_OK)
def get_activity(
        user_id: int,
        db: Session = Depends(repository.get_db)
):
    activity = repository.get_activity_by_user_id(db, user_id)
    return activity


@router.get("/get_activities/", status_code=status.HTTP_200_OK)
def get_activities(
        db: Session = Depends(repository.get_db)
):
    activities = repository.get_activities(db)
    return activities


@router.put("/update_activity/", status_code=status.HTTP_200_OK)
def update_activity(
        activity_create: schema.ActivityUpdate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    updated_activity = repository.update_activity(db, activity_create)

    return updated_activity


@router.put("/update_activity/", status_code=status.HTTP_200_OK)
def update_activity(
        activity_create: schema.ActivityUpdate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    activity_create.tour_guide_id = authenticate.get("user_id")

    response = repository.update_activity(db, activity_create)

    return response


@router.put("/delete_activity_by_id/", status_code=status.HTTP_200_OK)
def delete_activity(
        activity_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    response = repository.delete_activity_by_id(db, activity_id)

    return response


@router.get("/get_activity_by_filters/", status_code=status.HTTP_200_OK)
def get_activity_by_filters(
        activity_filter: schema.ActivityFilter,
        db: Session = Depends(repository.get_db)
):
    activities = repository.get_activity_by_filters(db, activity_filter)
    return activities


@router.delete("/delete_activity_by_id/", status_code=status.HTTP_200_OK)
def delete_activity_by_id(
        activity_id: int,
        db: Session = Depends(repository.get_db)
):
    response = repository.delete_activity_by_id(db, activity_id)
    return response


@router.delete("/delete_activity_by_tour_guide_id/", status_code=status.HTTP_200_OK)
def delete_activity_by_user_id(
        tour_guide_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    response = repository.delete_activity_by_user_id(db, tour_guide_id)
    return response


@router.post("/create_booking/", status_code=status.HTTP_200_OK)
def create_booking(
        booking_create: schema.BookingCreate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "user")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking_create.user_id = authenticate.get("user_id")
    booking = repository.create_booking(db, booking_create)
    return booking


@router.get("/get_booking_by_id/", status_code=status.HTTP_200_OK)
def get_booking_by_id(
        booking_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "user")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking = repository.get_booking_by_id(db, booking_id)
    return booking


@router.get("/get_booking_by_user_id/", status_code=status.HTTP_200_OK)
def get_booking_by_user_id(
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "user")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking = repository.get_booking_by_user_id(db, authenticate.get("user_id"))
    return booking


@router.get("/get_booking_by_activity_id/", status_code=status.HTTP_200_OK)
def get_booking_by_activity_id(
        activity_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking = repository.get_booking_by_activity_id(db, activity_id)
    return booking


@router.put("/update_booking/", status_code=status.HTTP_200_OK)
def update_booking(
        booking_create: schema.BookingUpdate,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "user")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking_create.user_id = authenticate.get("user_id")
    booking = repository.update_booking(db, booking_create)

    return booking


@router.delete("/delete_booking/", status_code=status.HTTP_200_OK)
def delete_booking(
        booking_id: int,
        token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
        db: Session = Depends(repository.get_db)
):
    authenticate = auth.authenticate(token.credentials, "user")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    booking = repository.delete_booking(db, booking_id)
    return booking
