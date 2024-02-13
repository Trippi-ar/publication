from fastapi import status, Depends, APIRouter

from sqlalchemy.orm import Session

from contextlib import contextmanager

from src.db_config import database
from src.models import models


router = APIRouter(
    tags=['Health Check']
)


@router.get("/sentry-debug", status_code=status.HTTP_200_OK)
async def trigger_error():
    """
    Verify the Sentry error tracking.
    """
    division_by_zero = 1 / 0


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Verify the health of services.
    """

    class UserRepository:
        @staticmethod
        @contextmanager
        def get_db() -> Session:
            db = database.SessionLocal()
            try:
                yield db
            finally:
                db.close()

    def test():
        with UserRepository.get_db() as db:
            try:
                db.query(models.Publication).first()
                return {"status": "ok", "message": "Database connection is healthy"}
            except Exception as e:
                return e

    return test()
