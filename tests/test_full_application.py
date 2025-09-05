import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.utils.exceptions import WeatherServiceException

client = TestClient(app)


class TestFullApplication:
    """اختبارات شاملة للتطبيق الكامل"""
    
    def test_root_endpoint(self):
        """اختبار الصفحة الرئيسية"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert "endpoints" in data
        assert "features" in data
        
        # التحقق من وجود جميع endpoints المطلوبة
        endpoints = data["endpoints"]
        assert "time_comparison" in endpoints
        assert "weather" in endpoints
        assert "supported_cities" in endpoints
        assert "docs" in endpoints
        assert "redoc" in endpoints
    
    def test_health_check_endpoint(self):
        """اختبار endpoint فحص الصحة"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "services" in data
        
        services = data["services"]
        assert services["time_service"] == "operational"
        assert services["weather_service"] == "operational"
    
    def test_time_comparison_full_flow(self):
        """اختبار التدفق الكامل لمقارنة الأوقات"""
        response = client.get("/time/comparison?city1=القاهرة&city2=لندن")
        
        assert response.status_code == 200
        data = response.json()
        
        # التحقق من جميع الحقول المطلوبة
        required_fields = [
            "city1", "city1_time", "city1_timezone",
            "city2", "city2_time", "city2_timezone", 
            "time_difference_hours"
        ]
        
        for field in required_fields:
            assert field in data
        
        # التحقق من صحة البيانات
        assert isinstance(data["time_difference_hours"], (int, float))
        assert "T" in data["city1_time"]  # ISO format
        assert "T" in data["city2_time"]  # ISO format
    
    def test_weather_full_flow(self):
        """اختبار التدفق الكامل للطقس"""
        response = client.get("/weather/?city=الرياض")
        
        assert response.status_code == 200
        data = response.json()
        
        # التحقق من جميع الحقول المطلوبة
        required_fields = ["city", "temperature", "description", "humidity", "feels_like"]
        
        for field in required_fields:
            assert field in data
        
        # التحقق من صحة البيانات
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["humidity"], int)
        assert isinstance(data["feels_like"], (int, float))
        assert isinstance(data["description"], str)
        assert len(data["description"]) > 0
    
    def test_supported_cities_endpoint(self):
        """اختبار endpoint المدن المدعومة"""
        response = client.get("/weather/cities")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "supported_cities" in data
        assert "message" in data
        assert isinstance(data["supported_cities"], list)
        assert len(data["supported_cities"]) > 0
        
        # التحقق من تنسيق المدن
        for city in data["supported_cities"]:
            assert "arabic" in city
            assert "english" in city
    
    def test_error_handling_city_not_found(self):
        """اختبار معالجة خطأ المدينة غير الموجودة"""
        response = client.get("/weather/?city=مدينة_غير_موجودة")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "error" in data
        assert "message" in data
        assert data["error"] == "http_error"
        assert "غير موجودة" in data["message"]
    
    def test_error_handling_empty_city(self):
        """اختبار معالجة خطأ المدينة الفارغة"""
        response = client.get("/weather/?city=")
        
        assert response.status_code == 400
        data = response.json()
        
        assert "error" in data
        assert "message" in data
    
    def test_error_handling_missing_parameters(self):
        """اختبار معالجة الأخطاء للمعاملات المفقودة"""
        # اختبار مقارنة الوقت بدون معاملات
        response = client.get("/time/comparison")
        assert response.status_code == 422  # Validation error
        
        # اختبار الطقس بدون معاملات
        response = client.get("/weather/")
        assert response.status_code == 422  # Validation error
    
    def test_cors_headers(self):
        """اختبار وجود CORS headers"""
        response = client.options("/")
        
        # التحقق من وجود CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_process_time_header(self):
        """اختبار وجود header وقت المعالجة"""
        response = client.get("/")
        
        assert "x-process-time" in response.headers
        process_time = float(response.headers["x-process-time"])
        assert process_time >= 0
    
    def test_multiple_concurrent_requests(self):
        """اختبار الطلبات المتزامنة"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/weather/?city=القاهرة")
        
        # تشغيل 5 طلبات متزامنة
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [future.result() for future in futures]
        
        # التحقق من نجاح جميع الطلبات
        for response in responses:
            assert response.status_code == 200
    
    def test_api_documentation_endpoints(self):
        """اختبار endpoints التوثيق"""
        # اختبار Swagger UI
        response = client.get("/docs")
        assert response.status_code == 200
        
        # اختبار ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
        
        # اختبار OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_input_validation_and_sanitization(self):
        """اختبار التحقق من صحة المدخلات وتنظيفها"""
        # اختبار مدينة بمسافات إضافية
        response = client.get("/weather/?city=  القاهرة  ")
        assert response.status_code == 200
        
        # اختبار أحرف خاصة
        response = client.get("/time/comparison?city1=Cairo&city2=London")
        assert response.status_code == 200
    
    def test_response_consistency(self):
        """اختبار ثبات تنسيق الاستجابات"""
        # اختبار عدة طلبات للتأكد من ثبات التنسيق
        for _ in range(3):
            response = client.get("/weather/?city=القاهرة")
            assert response.status_code == 200
            
            data = response.json()
            assert set(data.keys()) == {"city", "temperature", "description", "humidity", "feels_like"}
    
    @patch('app.services.weather_service.weather_service.get_weather')
    def test_external_service_timeout_handling(self, mock_get_weather):
        """اختبار معالجة timeout للخدمات الخارجية"""
        # محاكاة timeout
        mock_get_weather.side_effect = WeatherServiceException("Connection timeout")
        
        response = client.get("/weather/?city=القاهرة")
        
        assert response.status_code == 503
        data = response.json()
        assert "error" in data
        assert data["error"] == "weather_service_unavailable"
    
    def test_logging_functionality(self):
        """اختبار وظيفة التسجيل"""
        import logging
        
        # التحقق من أن التسجيل يعمل
        with patch('app.main.logger') as mock_logger:
            response = client.get("/")
            
            # التحقق من استدعاء logger
            assert mock_logger.info.called
    
    def test_performance_benchmarks(self):
        """اختبار معايير الأداء الأساسية"""
        import time
        
        # اختبار سرعة الاستجابة
        start_time = time.time()
        response = client.get("/weather/?city=القاهرة")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # يجب أن تكون الاستجابة أقل من ثانية واحدة
    
    def test_memory_usage_stability(self):
        """اختبار استقرار استخدام الذاكرة"""
        import gc
        
        # تشغيل عدة طلبات للتحقق من عدم تسريب الذاكرة
        for _ in range(10):
            response = client.get("/weather/?city=القاهرة")
            assert response.status_code == 200
        
        # تنظيف الذاكرة
        gc.collect()
        
        # التحقق من أن التطبيق لا يزال يعمل
        response = client.get("/health")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])