from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """إعدادات التطبيق"""
    weather_api_key: str = "your_api_key_here"
    weather_api_url: str = "https://api.openweathermap.org/data/2.5/weather"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


# إنشاء مثيل واحد من الإعدادات
settings = Settings()