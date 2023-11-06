from pydantic import BaseModel
from datetime import datetime


class ActivityCreate(BaseModel):
    name: str
    tour_guide_id: int = None
    difficulty: int
    distance: float
    date: datetime
    elevation: float
    price: float
    country: str
    administrative_area_level_1: str
    locality: str
    requirements: str
    information: str
    type: str


class ActivityById(BaseModel):
    id: int


class Activity(BaseModel):
    name: str
    tour_guide_id: int
    difficulty: int
    distance: float
    date: datetime
    desnivel: float
    price: float
    country: str
    administrative_area_level_1: str
    locality: str
    requirements: str
    information: str
    type: str


class LikeActivity(BaseModel):
    user_id: int
    activity_id: int
