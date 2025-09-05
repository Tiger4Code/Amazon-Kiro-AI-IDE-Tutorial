import httpx
import asyncio
from typing import Dict, Any
from ..utils.exceptions import CityNotFoundException, WeatherServiceException
from ..models.weather_models import WeatherResponse, WeatherData
from ..utils.config import settings


class WeatherService:
    """خدمة الطقس للحصول على معلومات الطقس من API خارجي"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.weather_api_key
        self.base_url = base_url or settings.weather_api_url
        self.timeout = 10.0  # مهلة زمنية للطلبات
        
        # ترجمة أوصاف الطقس من الإنجليزية للعربية
        self.weather_translations = {
            "clear sky": "سماء صافية",
            "few clouds": "غيوم قليلة", 
            "scattered clouds": "غيوم متناثرة",
            "broken clouds": "غيوم متكسرة",
            "shower rain": "أمطار متناثرة",
            "rain": "مطر",
            "thunderstorm": "عاصفة رعدية",
            "snow": "ثلج",
            "mist": "ضباب خفيف",
            "fog": "ضباب",
            "haze": "غبار",
            "overcast clouds": "غيوم كثيفة",
            "light rain": "مطر خفيف",
            "moderate rain": "مطر متوسط",
            "heavy rain": "مطر غزير"
        }
    
    async def get_weather_data(self, city_name: str) -> WeatherData:
        """الحصول على بيانات الطقس - حالياً ترجع بيانات ثابتة"""
        
        # قاموس البيانات الثابتة للمدن المختلفة
        mock_weather_data = {
            "cairo": {
                "main": {"temp": 28.5, "feels_like": 31.2, "humidity": 60},
                "weather": [{"description": "clear sky", "main": "Clear"}],
                "name": "Cairo",
                "cod": 200
            },
            "القاهرة": {
                "main": {"temp": 28.5, "feels_like": 31.2, "humidity": 60},
                "weather": [{"description": "clear sky", "main": "Clear"}],
                "name": "Cairo", 
                "cod": 200
            },
            "london": {
                "main": {"temp": 15.3, "feels_like": 14.1, "humidity": 78},
                "weather": [{"description": "overcast clouds", "main": "Clouds"}],
                "name": "London",
                "cod": 200
            },
            "لندن": {
                "main": {"temp": 15.3, "feels_like": 14.1, "humidity": 78},
                "weather": [{"description": "overcast clouds", "main": "Clouds"}],
                "name": "London",
                "cod": 200
            },
            "riyadh": {
                "main": {"temp": 35.2, "feels_like": 38.5, "humidity": 25},
                "weather": [{"description": "clear sky", "main": "Clear"}],
                "name": "Riyadh",
                "cod": 200
            },
            "الرياض": {
                "main": {"temp": 35.2, "feels_like": 38.5, "humidity": 25},
                "weather": [{"description": "clear sky", "main": "Clear"}],
                "name": "Riyadh",
                "cod": 200
            }
        }
        
        city_lower = city_name.lower().strip()
        
        if city_lower not in mock_weather_data:
            raise CityNotFoundException(city_name)
        
        # إرجاع البيانات الثابتة
        data = mock_weather_data[city_lower]
        return WeatherData(**data)
        
        # TODO: عند الاشتراك في خدمة الطقس، استبدل الكود أعلاه بالكود التالي:
        # params = {
        #     "q": city_name,
        #     "appid": self.api_key,
        #     "units": "metric",
        #     "lang": "en"
        # }
        # async with httpx.AsyncClient(timeout=self.timeout) as client:
        #     response = await client.get(self.base_url, params=params)
        #     # معالجة الاستجابة...
    
    def format_weather_response(self, raw_data: WeatherData) -> WeatherResponse:
        """تنسيق استجابة الطقس وترجمة الأوصاف"""
        try:
            # استخراج البيانات الأساسية
            main_data = raw_data.main
            weather_data = raw_data.weather[0] if raw_data.weather else {}
            
            # ترجمة وصف الطقس
            description_en = weather_data.get("description", "").lower()
            description_ar = self.weather_translations.get(
                description_en, 
                description_en  # إذا لم توجد ترجمة، استخدم النص الإنجليزي
            )
            
            return WeatherResponse(
                city=raw_data.name,
                temperature=round(main_data.get("temp", 0), 1),
                description=description_ar,
                humidity=main_data.get("humidity", 0),
                feels_like=round(main_data.get("feels_like", 0), 1)
            )
        except Exception as e:
            raise WeatherServiceException(f"خطأ في تنسيق بيانات الطقس: {str(e)}")
    
    async def get_weather(self, city_name: str) -> WeatherResponse:
        """الحصول على معلومات الطقس المنسقة لمدينة معينة"""
        try:
            raw_data = await self.get_weather_data(city_name)
            return self.format_weather_response(raw_data)
        except (CityNotFoundException, WeatherServiceException):
            raise
        except Exception as e:
            raise WeatherServiceException(f"خطأ في الحصول على بيانات الطقس: {str(e)}")


# إنشاء مثيل واحد من خدمة الطقس
weather_service = WeatherService()