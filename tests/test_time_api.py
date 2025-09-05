import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestTimeAPI:
    """اختبارات API الوقت"""
    
    def test_compare_times_success(self):
        """اختبار مقارنة الأوقات بنجاح"""
        response = client.get("/time/comparison?city1=Cairo&city2=London")
        
        assert response.status_code == 200
        data = response.json()
        
        # التحقق من وجود جميع الحقول المطلوبة
        assert "city1" in data
        assert "city1_time" in data
        assert "city1_timezone" in data
        assert "city2" in data
        assert "city2_time" in data
        assert "city2_timezone" in data
        assert "time_difference_hours" in data
        
        # التحقق من القيم
        assert data["city1"] == "Cairo"
        assert data["city2"] == "London"
        assert data["city1_timezone"] == "Africa/Cairo"
        assert data["city2_timezone"] == "Europe/London"
        assert isinstance(data["time_difference_hours"], (int, float))
    
    def test_compare_times_arabic_cities(self):
        """اختبار مقارنة الأوقات بأسماء عربية"""
        response = client.get("/time/comparison?city1=القاهرة&city2=الرياض")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["city1"] == "القاهرة"
        assert data["city2"] == "الرياض"
        assert data["city1_timezone"] == "Africa/Cairo"
        assert data["city2_timezone"] == "Asia/Riyadh"
    
    def test_compare_times_missing_city1(self):
        """اختبار مقارنة الأوقات مع مدينة أولى مفقودة"""
        response = client.get("/time/comparison?city2=London")
        
        assert response.status_code == 422
    
    def test_compare_times_missing_city2(self):
        """اختبار مقارنة الأوقات مع مدينة ثانية مفقودة"""
        response = client.get("/time/comparison?city1=Cairo")
        
        assert response.status_code == 422
    
    def test_compare_times_empty_city1(self):
        """اختبار مقارنة الأوقات مع مدينة أولى فارغة"""
        response = client.get("/time/comparison?city1=&city2=London")
        
        assert response.status_code == 500
        data = response.json()
        assert response.status_code == 500  # تأكد من رمز الحالة فقط
    
    def test_compare_times_empty_city2(self):
        """اختبار مقارنة الأوقات مع مدينة ثانية فارغة"""
        response = client.get("/time/comparison?city1=Cairo&city2=")
        
        assert response.status_code == 500
        data = response.json()
        assert response.status_code == 500  # تأكد من رمز الحالة فقط
    
    def test_compare_times_invalid_city(self):
        """اختبار مقارنة الأوقات مع مدينة غير موجودة"""
        response = client.get("/time/comparison?city1=Cairo&city2=مدينة_غير_موجودة")
        
        assert response.status_code == 400
        data = response.json()
        assert "City not found" in data["error"] or data["error"] == "http_error"
        # تأكد من وجود رسالة خطأ مناسبة
        assert response.status_code == 400
    
    def test_compare_times_case_insensitive(self):
        """اختبار أن أسماء المدن غير حساسة لحالة الأحرف"""
        response = client.get("/time/comparison?city1=CAIRO&city2=london")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["city1"] == "CAIRO"
        assert data["city2"] == "london"
        assert data["city1_timezone"] == "Africa/Cairo"
        assert data["city2_timezone"] == "Europe/London"
    
    def test_compare_times_same_city(self):
        """اختبار مقارنة الأوقات لنفس المدينة"""
        response = client.get("/time/comparison?city1=Cairo&city2=Cairo")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["time_difference_hours"] == 0.0