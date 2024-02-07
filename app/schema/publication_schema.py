from fastapi import UploadFile, File, Form

from dataclasses import dataclass
from pydantic import BaseModel, constr, validator, Field, UUID4
from datetime import date, datetime

from typing import List, Optional


@dataclass
class Request:
    name: str = Form()
    difficulty: str = Form()
    distance: float = Form(..., gt=0)
    duration: int = Form(..., gt=0)
    price: float = Form(..., gt=0)
    description: str = Form()
    tools: str = Form()
    type: str = Form()
    languages: List[str] = Form()
    max_participants: int = Form(..., gt=0)
    dates: List[str] = Form()
    images: List[UploadFile] = File(...)
    country: str = Form()
    administrative_area_level_1: str = Form()
    locality: str = Form()


class Create(BaseModel):
    tour_guide_id: UUID4
    name: str
    difficulty: str
    distance: float
    duration: int
    price: float
    description: str
    tools: str
    type: str
    languages: List[str]
    max_participants: int
    dates: List[str]
    images: List[str]
    country: str
    administrative_area_level_1: str
    locality: str

    class Config:
        orm_mode = True


class CreateResponse(Create):
    id: UUID4
    created_at: datetime


class Params(BaseModel):
    id: Optional[UUID4] = None
    name: Optional[str] = None


class GetResponse(BaseModel):
    id: UUID4
    name: str
    difficulty: str
    distance: float
    duration: int
    price: float
    description: str
    tools: str
    type: str
    languages: List[str]
    max_participants: int
    dates: List[str]
    images: List[str]
    country: str
    administrative_area_level_1: str
    locality: str
    full_address: str


class Pagination(BaseModel):
    per_page: int
    page: int


class Filter(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    difficulty: Optional[str] = None
    max_distance: Optional[float] = None
    min_distance: Optional[float] = None
    max_duration: Optional[int] = None
    min_duration: Optional[int] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    country: Optional[str] = None
    administrative_area_level_1: Optional[str] = None
    locality: Optional[str] = None
    languages: Optional[str] = None
    available_spots: Optional[int] = None


class Suggestions(BaseModel):
    name: List[str]
    full_address: List[str]



