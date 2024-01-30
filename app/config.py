import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_URI = os.getenv("DATABASE_URI_ACTIVITY")
    AUTH_URL = os.getenv("AUTH_URL")


settings = Settings()
