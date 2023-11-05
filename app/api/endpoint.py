from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repository import repository

from app.schema import schema

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/activity",
    tags=['Activity']
)


@router.post(
    "/", status_code=status.HTTP_200_OK
)
def create_activity(
    activity_create:schema.ActivityCreate,
    db: Session = Depends(repository.get_db)
):

    activity_created = repository.create_activity(db, activity_create)

    return

