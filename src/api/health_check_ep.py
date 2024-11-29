from fastapi import status, Depends, APIRouter

from sqlalchemy.orm import Session

from contextlib import contextmanager

from src.db_config import database
from src.models import models
from src.config import configure_firebase

router = APIRouter(
    tags=['Health Check']
)

@contextmanager
def db_session() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/db", status_code=status.HTTP_200_OK)
async def check_db():
    """
    Verify the health of services.
    """
    try:
        with db_session() as db:
            db.connection() 
            return {"status": "ok", "message": "Database connection is healthy"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}


@router.get("/firebase", status_code=status.HTTP_200_OK)
async def check_firebase():
    """
    Verify the health of services.
    """
    try:
        firebase = configure_firebase()
        storage = firebase.storage()
        storage.child("test-health-check").get_url(token=None)
        return {"status": "ok", "message": "Firebase connection is healthy"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"Firebase connection failed: {str(e)}"}
        )