from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import sentry_sdk

import pyrebase

import os


def configure_cors(app: FastAPI):
    origins = [
        "http://localhost:8080",
    ]
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_sentry(app: FastAPI):
    sentry_sdk.init(
        dsn=Settings.DSN_SENTRY,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    app.add_middleware(SentryAsgiMiddleware)


def configure_firebase():
    config = {
        "apiKey": Settings.API_KEY_FIREBASE,
        "authDomain": Settings.AUTH_DOMAIN_FIREBASE,
        "projectId": Settings.PROJECT_ID_FIREBASE,
        "storageBucket": Settings.STORAGE_BUCKET_FIREBASE,
        "messagingSenderId": Settings.MESSAGING_SENDER_ID_FIREBASE,
        "appId": Settings.APP_ID_FIREBASE,
        "databaseURL": Settings.DATABASE_URL_FIREBASE,
        "serviceAccount": "firebaseCredentials.json"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase


class Settings:
    if os.getenv("ENVIRONMENT") == "dev-local":
        DATABASE_URI = os.getenv("DATABASE_URI_LOCAL")
    else:
        DATABASE_URI = os.getenv("DATABASE_URI")

    DSN_SENTRY = os.getenv("DSN_SENTRY")

    API_KEY_FIREBASE = os.getenv("API_KEY_FIREBASE")
    AUTH_DOMAIN_FIREBASE = os.getenv("AUTH_DOMAIN_FIREBASE")
    PROJECT_ID_FIREBASE = os.getenv("PROJECT_ID_FIREBASE")
    STORAGE_BUCKET_FIREBASE = os.getenv("STORAGE_BUCKET_FIREBASE")
    MESSAGING_SENDER_ID_FIREBASE = int(os.getenv("MESSAGING_SENDER_ID_FIREBASE"))
    APP_ID_FIREBASE = os.getenv("APP_ID_FIREBASE")
    DATABASE_URL_FIREBASE = os.getenv("DATABASE_URL_FIREBASE")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    AUTH_URL = os.getenv("AUTH_URL")


settings = Settings()
