from pydantic import BaseModel
from typing import Optional


class TimeInfo(BaseModel):
    """معلومات الوقت لمدينة واحدة"""
    city: str
    current_time: str
    timezone: str


class TimeComparisonResponse(BaseModel):
    """استجابة مقارنة الأوقات بين مدينتين"""
    city1: str
    city1_time: str
    city1_timezone: str
    city2: str
    city2_time: str
    city2_timezone: str
    time_difference_hours: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "city1": "Cairo",
                "city1_time": "2024-01-15T14:30:00",
                "city1_timezone": "Africa/Cairo",
                "city2": "London",
                "city2_time": "2024-01-15T12:30:00",
                "city2_timezone": "Europe/London",
                "time_difference_hours": 2.0
            }
        }