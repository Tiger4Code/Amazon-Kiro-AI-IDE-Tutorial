from datetime import datetime
import pytz
from typing import Dict, Tuple
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from ..utils.exceptions import CityNotFoundException, TimezoneNotFoundException
from ..models.time_models import TimeInfo, TimeComparisonResponse


class TimeService:
    """خدمة الوقت والمناطق الزمنية"""
    
    def __init__(self):
        # إعداد أدوات البحث الجغرافي
        self.geolocator = Nominatim(user_agent="fastapi-time-weather")
        self.tf = TimezoneFinder()
        
        # قاموس المدن الشائعة للبحث السريع (اختياري)
        self.city_timezones = {
            # مدن عربية
            "cairo": "Africa/Cairo",
            "القاهرة": "Africa/Cairo",
            "riyadh": "Asia/Riyadh", 
            "الرياض": "Asia/Riyadh",
            "dubai": "Asia/Dubai",
            "دبي": "Asia/Dubai",
            "beirut": "Asia/Beirut",
            "بيروت": "Asia/Beirut",
            "baghdad": "Asia/Baghdad",
            "بغداد": "Asia/Baghdad",
            "damascus": "Asia/Damascus",
            "دمشق": "Asia/Damascus",
            "amman": "Asia/Amman",
            "عمان": "Asia/Amman",
            
            # مدن عالمية
            "london": "Europe/London",
            "لندن": "Europe/London",
            "paris": "Europe/Paris",
            "باريس": "Europe/Paris",
            "new york": "America/New_York",
            "نيويورك": "America/New_York",
            "tokyo": "Asia/Tokyo",
            "طوكيو": "Asia/Tokyo",
            "moscow": "Europe/Moscow",
            "موسكو": "Europe/Moscow",
            "sydney": "Australia/Sydney",
            "سيدني": "Australia/Sydney"
        }
    
    def get_city_timezone(self, city_name: str) -> str:
        """الحصول على المنطقة الزمنية للمدينة - يدعم أي مدينة في العالم"""
        city_lower = city_name.lower().strip()
        
        # أولاً: جرب البحث في القاموس السريع للمدن الشائعة
        if city_lower in self.city_timezones:
            return self.city_timezones[city_lower]
        
        # ثانياً: ابحث عن المدينة جغرافياً
        try:
            location = self.geolocator.geocode(city_name, timeout=10)
            if location is None:
                raise CityNotFoundException(city_name)
            
            # احصل على المنطقة الزمنية من الإحداثيات
            timezone_str = self.tf.timezone_at(lat=location.latitude, lng=location.longitude)
            if timezone_str is None:
                raise CityNotFoundException(city_name)
                
            return timezone_str
            
        except Exception as e:
            raise CityNotFoundException(city_name)
    
    def get_current_time_in_city(self, city_name: str) -> TimeInfo:
        """الحصول على الوقت الحالي في مدينة معينة"""
        try:
            timezone_name = self.get_city_timezone(city_name)
            timezone = pytz.timezone(timezone_name)
            current_time = datetime.now(timezone)
            
            return TimeInfo(
                city=city_name,
                current_time=current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                timezone=timezone_name
            )
        except CityNotFoundException:
            raise
        except Exception as e:
            raise TimezoneNotFoundException(city_name)
    
    def calculate_time_difference(self, city1: str, city2: str) -> TimeComparisonResponse:
        """حساب فرق التوقيت بين مدينتين"""
        try:
            # الحصول على معلومات الوقت للمدينة الأولى
            time_info1 = self.get_current_time_in_city(city1)
            timezone1 = pytz.timezone(time_info1.timezone)
            current_time1 = datetime.now(timezone1)
            
            # الحصول على معلومات الوقت للمدينة الثانية  
            time_info2 = self.get_current_time_in_city(city2)
            timezone2 = pytz.timezone(time_info2.timezone)
            current_time2 = datetime.now(timezone2)
            
            # حساب فرق التوقيت بالساعات
            time_diff = (current_time1.utcoffset().total_seconds() - 
                        current_time2.utcoffset().total_seconds()) / 3600
            
            return TimeComparisonResponse(
                city1=city1,
                city1_time=current_time1.strftime("%Y-%m-%dT%H:%M:%S"),
                city1_timezone=time_info1.timezone,
                city2=city2,
                city2_time=current_time2.strftime("%Y-%m-%dT%H:%M:%S"),
                city2_timezone=time_info2.timezone,
                time_difference_hours=round(time_diff, 1)
            )
        except (CityNotFoundException, TimezoneNotFoundException):
            raise
        except Exception as e:
            raise TimezoneNotFoundException(f"{city1} أو {city2}")


# إنشاء مثيل واحد من الخدمة
time_service = TimeService()