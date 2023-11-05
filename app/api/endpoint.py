from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repository import repository

from app.schema import schema
from app.auth import auth

token_auth_scheme = HTTPBearer()

router = APIRouter(
    prefix="/api/activity",
    tags=['Activity']
)


@router.post(
    "/", status_code=status.HTTP_200_OK
)
def create_activity(
    activity_create: schema.ActivityCreate,
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
    db: Session = Depends(repository.get_db)
):

    authenticate = auth.authenticate(token.credentials, "guide")
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas"
        )

    activity_create.tour_guide_id = authenticate.get("user_id")

    activity_created = repository.create_activity(db, activity_create)

    return

