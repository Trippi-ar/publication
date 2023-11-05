from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityCreate(BaseModel):
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

