import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_URI = os.getenv("DATABASE_URI_ACTIVITY")
    AUTH_URL = os.getenv("AUTH_URL")
    API_KEY_FIREBASE= os.getenv("API_KEY_FIREBASE")
    AUTH_DOMAIN_FIREBASE= os.getenv("AUTH_DOMAIN_FIREBASE")
    PROJECT_ID_FIREBASE= os.getenv("PROJECT_ID_FIREBASE")
    STORAGE_BUCKET_FIREBASE= os.getenv("STORAGE_BUCKET_FIREBASE")
    MESSAGING_SENDER_ID_FIREBASE= int(os.getenv("MESSAGING_SENDER_ID_FIREBASE"))
    APP_ID_FIREBASE= os.getenv("APP_ID_FIREBASE")
    DATABASE_URL_FIREBASE= os.getenv("DATABASE_URL_FIREBASE")


settings = Settings()
