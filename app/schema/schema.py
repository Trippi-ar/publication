from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    token: Optional[str]
    role: Optional[str]
    expiration_date: Optional[datetime]
    is_active: Optional[bool]
    user_id: Optional[int]



