from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.auth import auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_and_authorize(credentials, role):
    authenticate = auth.authenticate(credentials, role)
    if authenticate is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )