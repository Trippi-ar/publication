from fastapi import FastAPI, status

from src.api import publication_ep, booking_ep, health_ep
from src.config import configure_cors, configure_sentry

app = FastAPI()

configure_cors(app)
configure_sentry(app)

app.include_router(publication_ep.router)
app.include_router(booking_ep.router)
app.include_router(health_ep.router)
