from pydantic_settings import BaseSettings
import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    PASSWORD_EMAIL = os.getenv("PASSWORD_EMAIL")
    SECRET_KEY_EMAIL = os.getenv("SECRET_KEY_EMAIL")
    ALGORITHM_EMAIL = os.getenv("ALGORITHM_EMAIL")
    DATABASE_URI_BOOKING = os.getenv("DATABASE_URI_ACTIVITY")
    PUBLICATIONS_LOCALHOST = os.getenv("ACTIVITY_LOCALHOST")
    USERS_LOCALHOST = os.getenv("USERS_LOCALHOST")


settings = Settings()
