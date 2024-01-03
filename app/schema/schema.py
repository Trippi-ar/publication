from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseModel):
    name: str
    tour_guide_id: int = None
    difficulty: int
    distance: float
    date: datetime
    elevation: float
    duration: int
    price: float
    languages: str
    transport: str
    description: str
    tools: str
    itinerary: str
    country: str
    administrative_area_level_1: str
    locality: str
    type: str


class ActivityUpdate(BaseModel):
    difficulty: int
    distance: float
    date: datetime
    elevation: float
    duration: int
    price: float
    languages: str
    transport: str
    description: str
    tools: str
    itinerary: str
    country: str
    administrative_area_level_1: str
    locality: str
    type: str
    activity_id: int


class ActivityFilter(BaseModel):
    name: Optional[str]
    tour_guide_id: Optional[int]
    difficulty: Optional[int]
    distance: Optional[float]
    date: Optional[datetime]
    elevation: Optional[float]
    duration: Optional[int]
    price: Optional[float]
    languages: Optional[str]
    transport: Optional[str]
    description: Optional[str]
    tools: Optional[str]
    itinerary: Optional[str]
    country: Optional[str]
    administrative_area_level_1: Optional[str]
    locality: Optional[str]
    type: Optional[str]


class BookingCreate(BaseModel):
    activity_id: int
    date: datetime
    number_people: int
    price: float
    user_id: int


class BookingUpdate(BaseModel):
    booking_id: int
    date: datetime
    number_people: int
    price: float
    state: str
