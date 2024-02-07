from pydantic import BaseModel, UUID4

from datetime import date


class Availability(BaseModel):
    publication_id: UUID4
    date: date
    participant: int


class Request(BaseModel):
    publication_id: UUID4
    date: date
    participant: int


class Create(Request):
    user_id: UUID4


class Response(BaseModel):
    id: UUID4
    name: str
    user_id: UUID4
    date: date
    participant: int
    price: float
    state: str
    created_at: date
