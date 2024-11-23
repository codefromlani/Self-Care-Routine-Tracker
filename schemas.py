from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date
from enum import Enum


# Enum for categories
class CategoryEnum(str, Enum):
    MEDITATION = "meditation"
    EXERCISE = "exercise"
    READING = "reading"
    JOURNALING = "journaling"
    NUTRITION = "nutrition"
    OTHER = "other"

# Pydantic model
class SelfCareActivity(BaseModel):
    id: Optional[int] = None
    activity_name: str
    duration_minutes: int
    date: date
    category: CategoryEnum
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "activity_name": "Morning Meditation",
                "duration_minutes": 15,
                "date": "2024-11-12",
                "category": "meditation",
                "notes": "Felt very peaceful today"
            }
        }

class ActivityResponse(SelfCareActivity):

    class config:
        orm_mode: True

class ActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    duration_minutes: Optional[int] = None
    date: Optional[str] = None 
    category: Optional[CategoryEnum] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True 

class ActivityStats(BaseModel):
    total_activities: int
    total_duration_minutes: int
    activities_by_category: Dict[str, int]
    average_duration: float
    streak_days: int