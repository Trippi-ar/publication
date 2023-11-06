from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


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


class DeleteActivity(BaseModel):
    user_id: int = None
    activity_id: int


class ActivityDetails(BaseModel):
    type: str
    requirements: str
    information: str


class ActivityWithDetails(BaseModel):
    activity_id: int
    name: str
    tour_guide_id: int
    difficulty: int
    distance: float
    date: datetime
    elevation: float
    price: float
    details: ActivityDetails



class MultiplesActivities(BaseModel):
    activities: List[ActivityWithDetails] = []

    def reply_to_dict(self, activity: ActivityWithDetails):
        details: activity.details
        return {
            "activity_id": activity.tour_guide_id,  # Replace with the correct attribute for activity_id
            "name": activity.name,
            "tour_guide_id": activity.tour_guide_id,
            "difficulty": activity.difficulty,
            "distance": activity.distance,
            "date": activity.date,
            "elevation": activity.desnivel,
            "price": activity.price,
            "details": {
                "type": details.type,
                "requirements": details.requirements,
                "information": details.information,
            }
        }

    def get_all_activities(self):
        return self.activities
