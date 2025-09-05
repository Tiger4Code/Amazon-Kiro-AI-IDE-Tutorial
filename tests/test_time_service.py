import pytest
from datetime import datetime
import pytz
from app.services.time_service import TimeService
from app.utils.exceptions import CityNotFoundException, TimezoneNotFoundException


class TestTimeService:
    """اختبارات خدمة الوقت"""
    
    def setup_method(self):
        """إعداد الاختبارات"""
        self.time_service = TimeService()
    
    def test_get_city_timezone_valid_city(self):
        """اختبار الحصول على المنطقة الزمنية لمدينة صحيحة"""
        timezone = self.time_service.get_city_timezone("cairo")
        assert timezone == "Africa/Cairo"
        
        timezone_ar = self.time_service.get_city_timezone("القاهرة")
        assert timezone_ar == "Africa/Cairo"
    
    def test_get_city_timezone_invalid_city(self):
        """اختبار الحصول على المنطقة الزمنية لمدينة غير موجودة"""
        with pytest.raises(CityNotFoundException):
            self.time_service.get_city_timezone("مدينة_غير_موجودة")
    
    def test_get_current_time_in_city_valid(self):
        """اختبار الحصول على الوقت الحالي لمدينة صحيحة"""
        time_info = self.time_service.get_current_time_in_city("london")
        
        assert time_info.city == "london"
        assert time_info.timezone == "Europe/London"
        assert isinstance(time_info.current_time, str)
        # التحقق من تنسيق التاريخ
        datetime.fromisoformat(time_info.current_time)
    
    def test_get_current_time_in_city_invalid(self):
        """اختبار الحصول على الوقت لمدينة غير موجودة"""
        with pytest.raises(CityNotFoundException):
            self.time_service.get_current_time_in_city("مدينة_خيالية")    def
 test_calculate_time_difference_valid_cities(self):
        """اختبار حساب فرق التوقيت بين مدينتين صحيحتين"""
        comparison = self.time_service.calculate_time_difference("cairo", "london")
        
        assert comparison.city1 == "cairo"
        assert comparison.city2 == "london"
        assert comparison.city1_timezone == "Africa/Cairo"
        assert comparison.city2_timezone == "Europe/London"
        assert isinstance(comparison.time_difference_hours, float)
        
        # التحقق من تنسيق التواريخ
        datetime.fromisoformat(comparison.city1_time)
        datetime.fromisoformat(comparison.city2_time)
    
    def test_calculate_time_difference_invalid_city(self):
        """اختبار حساب فرق التوقيت مع مدينة غير موجودة"""
        with pytest.raises(CityNotFoundException):
            self.time_service.calculate_time_difference("cairo", "مدينة_غير_موجودة")
    
    def test_case_insensitive_city_names(self):
        """اختبار أن أسماء المدن غير حساسة لحالة الأحرف"""
        timezone1 = self.time_service.get_city_timezone("CAIRO")
        timezone2 = self.time_service.get_city_timezone("cairo")
        timezone3 = self.time_service.get_city_timezone("Cairo")
        
        assert timezone1 == timezone2 == timezone3 == "Africa/Cairo"