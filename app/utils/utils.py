import requests

from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.config import Settings
from app.utils import errors

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate(token: str, role_request: str):
    payload = {"token": token, "role_request": role_request}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(Settings.AUTH_URL, headers=headers, json=payload)

    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise errors.AuthenticationError
