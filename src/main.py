from fastapi import FastAPI, status, Depends, HTTPException


from src.api import publication_ep, booking_ep, health_check_ep
from src.config import configure_cors

app = FastAPI()

configure_cors(app)

app.include_router(publication_ep.router)
app.include_router(booking_ep.router)
app.include_router(health_check_ep.router)