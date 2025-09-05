import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.weather_models import WeatherResponse
from app.utils.exceptions import CityNotFoundException, WeatherServiceException

client = TestClient(app)


class TestWeatherAPI:
    """اختبارات API الطقس"""
    
    def test_get_weather_success_arabic_city(self):
        """اختبار الحصول على الطقس بنجاح لمدينة عربية"""
        response = client.get("/weather/?city=القاهرة")
        
        assert response.status_code == 200
        data = response.json()
        
        # التحقق من وجود الحقول المطلوبة
        assert "city" in data
        assert "temperature" in data
        assert "description" in data
        assert "humidity" in data
        assert "feels_like" in data
        
        # التحقق من أن الوصف باللغة العربية
        assert isinstance(data["description"], str)
        assert len(data["description"]) > 0
    
    def test_get_weather_success_english_city(self):
        """اختبار الحصول على الطقس بنجاح لمدينة إنجليزية"""
        response = client.get("/weather/?city=London")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["city"] == "London"
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["humidity"], int)
        assert isinstance(data["feels_like"], (int, float))
    
    def test_get_weather_city_not_found(self):
        """اختبار حالة المدينة غير الموجودة"""
        response = client.get("/weather/?city=مدينة_غير_موجودة")
        
        assert response.status_code == 404
        data = response.json()
        assert "المدينة" in data["detail"]
        assert "غير موجودة" in data["detail"]
    
    def test_get_weather_empty_city(self):
        """اختبار حالة اسم المدينة فارغ"""
        response = client.get("/weather/?city=")
        
        assert response.status_code == 400
        data = response.json()
        assert "يجب تحديد اسم المدينة" in data["detail"]
    
    def test_get_weather_missing_city_parameter(self):
        """اختبار حالة عدم وجود معامل المدينة"""
        response = client.get("/weather/")
        
        assert response.status_code == 422  # Validation error
    
    def test_get_weather_whitespace_city(self):
        """اختبار حالة اسم المدينة يحتوي على مسافات فقط"""
        response = client.get("/weather/?city=   ")
        
        assert response.status_code == 400
        data = response.json()
        assert "يجب تحديد اسم المدينة" in data["detail"]
    
    @patch('app.services.weather_service.weather_service.get_weather')
    def test_get_weather_service_exception(self, mock_get_weather):
        """اختبار حالة خطأ في خدمة الطقس"""
        mock_get_weather.side_effect = WeatherServiceException("خطأ في الاتصال بالخدمة")
        
        response = client.get("/weather/?city=القاهرة")
        
        assert response.status_code == 503
        data = response.json()
        assert "خطأ في خدمة الطقس" in data["detail"]
    
    @patch('app.services.weather_service.weather_service.get_weather')
    def test_get_weather_internal_error(self, mock_get_weather):
        """اختبار حالة خطأ داخلي غير متوقع"""
        mock_get_weather.side_effect = Exception("خطأ غير متوقع")
        
        response = client.get("/weather/?city=القاهرة")
        
        assert response.status_code == 500
        data = response.json()
        assert "حدث خطأ داخلي في الخادم" in data["detail"]
    
    def test_get_supported_cities(self):
        """اختبار الحصول على قائمة المدن المدعومة"""
        response = client.get("/weather/cities")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "supported_cities" in data
        assert "message" in data
        assert isinstance(data["supported_cities"], list)
        assert len(data["supported_cities"]) > 0
        
        # التحقق من وجود المدن المطلوبة
        cities = data["supported_cities"]
        city_names = [city["arabic"] for city in cities] + [city["english"] for city in cities]
        
        assert "القاهرة" in city_names
        assert "Cairo" in city_names
        assert "الرياض" in city_names
        assert "Riyadh" in city_names
    
    def test_weather_response_format(self):
        """اختبار تنسيق استجابة الطقس"""
        response = client.get("/weather/?city=الرياض")
        
        assert response.status_code == 200
        data = response.json()
        
        # التحقق من أنواع البيانات
        assert isinstance(data["city"], str)
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["description"], str)
        assert isinstance(data["humidity"], int)
        assert isinstance(data["feels_like"], (int, float))
        
        # التحقق من القيم المنطقية
        assert -50 <= data["temperature"] <= 60  # درجة حرارة منطقية
        assert 0 <= data["humidity"] <= 100      # رطوبة منطقية
        assert -60 <= data["feels_like"] <= 70   # الشعور بالحرارة منطقي
    
    def test_weather_api_documentation(self):
        """اختبار توثيق API"""
        # اختبار أن endpoint موجود في التوثيق
        response = client.get("/docs")
        assert response.status_code == 200
        
        # اختبار OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        paths = schema.get("paths", {})
        
        # التحقق من وجود مسارات الطقس
        assert "/weather/" in paths
        assert "/weather/cities" in paths


if __name__ == "__main__":
    pytest.main([__file__])