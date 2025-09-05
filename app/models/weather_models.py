from pydantic import BaseModel
from typing import List, Dict, Any


class WeatherResponse(BaseModel):
    """استجابة معلومات الطقس"""
    city: str
    temperature: float
    description: str
    humidity: int
    feels_like: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "Cairo",
                "temperature": 25.5,
                "description": "غائم جزئياً",
                "humidity": 65,
                "feels_like": 27.2
            }
        }


class WeatherData(BaseModel):
    """نموذج البيانات الخام من API الطقس"""
    main: Dict[str, Any]
    weather: List[Dict[str, Any]]
    name: str
    cod: int