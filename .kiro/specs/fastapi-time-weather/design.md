# وثيقة التصميم

## نظرة عامة

تطبيق FastAPI يوفر خدمتين رئيسيتين: مقارنة الأوقات بين المدن والحصول على معلومات الطقس. التطبيق مصمم ليكون بسيطاً وقابلاً للصيانة مع معالجة شاملة للأخطاء.

## البنية المعمارية

### البنية العامة
```
fastapi-time-weather/
├── app/
│   ├── __init__.py
│   ├── main.py              # نقطة دخول التطبيق
│   ├── models/
│   │   ├── __init__.py
│   │   ├── time_models.py   # نماذج بيانات الوقت
│   │   └── weather_models.py # نماذج بيانات الطقس
│   ├── services/
│   │   ├── __init__.py
│   │   ├── time_service.py  # خدمة الوقت والمناطق الزمنية
│   │   └── weather_service.py # خدمة الطقس
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── time_router.py   # مسارات API للوقت
│   │   └── weather_router.py # مسارات API للطقس
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py    # استثناءات مخصصة
│       └── config.py        # إعدادات التطبيق
├── tests/
│   ├── __init__.py
│   ├── test_time_api.py
│   └── test_weather_api.py
├── requirements.txt
└── .env                     # متغيرات البيئة
```

### نمط المعمارية
- **Layered Architecture**: فصل الاهتمامات بين الطبقات
- **Service Layer Pattern**: منطق العمل في طبقة الخدمات
- **Repository Pattern**: (مبسط) للوصول للبيانات الخارجية

## المكونات والواجهات

### 1. طبقة API (Routers)

#### Time Router (`/time-comparison`)
- **المسار**: `GET /time-comparison?city1={city1}&city2={city2}`
- **المدخلات**: اسم مدينتين كمعاملات استعلام
- **المخرجات**: JSON يحتوي على الأوقات وفرق التوقيت

#### Weather Router (`/weather`)
- **المسار**: `GET /weather?city={city}`
- **المدخلات**: اسم مدينة كمعامل استعلام
- **المخرجات**: JSON يحتوي على معلومات الطقس

### 2. طبقة الخدمات (Services)

#### Time Service
```python
class TimeService:
    def get_city_timezone(self, city_name: str) -> str
    def get_current_time_in_city(self, city_name: str) -> datetime
    def calculate_time_difference(self, city1: str, city2: str) -> dict
```

#### Weather Service
```python
class WeatherService:
    def __init__(self, api_key: str, base_url: str)
    def get_weather_data(self, city_name: str) -> dict
    def format_weather_response(self, raw_data: dict) -> dict
```

### 3. طبقة النماذج (Models)

#### Time Models
```python
class TimeComparisonResponse(BaseModel):
    city1: str
    city1_time: str
    city1_timezone: str
    city2: str
    city2_time: str
    city2_timezone: str
    time_difference_hours: float

class TimeInfo(BaseModel):
    city: str
    current_time: str
    timezone: str
```

#### Weather Models
```python
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    feels_like: float

class WeatherData(BaseModel):
    main: dict
    weather: list
    name: str
```

## نماذج البيانات

### استجابة مقارنة الأوقات
```json
{
    "city1": "Cairo",
    "city1_time": "2024-01-15T14:30:00",
    "city1_timezone": "Africa/Cairo",
    "city2": "London", 
    "city2_time": "2024-01-15T12:30:00",
    "city2_timezone": "Europe/London",
    "time_difference_hours": 2.0
}
```

### استجابة الطقس
```json
{
    "city": "Cairo",
    "temperature": 25.5,
    "description": "غائم جزئياً",
    "humidity": 65,
    "feels_like": 27.2
}
```

### نماذج الأخطاء
```json
{
    "error": "City not found",
    "message": "المدينة المطلوبة غير موجودة",
    "status_code": 400
}
```

## معالجة الأخطاء

### أنواع الأخطاء المتوقعة

1. **خطأ المدينة غير الموجودة** (400)
   - عندما لا يتم العثور على المدينة في قاعدة بيانات المناطق الزمنية
   - عندما تفشل خدمة الطقس في العثور على المدينة

2. **خطأ خدمة خارجية** (503)
   - عندما تفشل خدمة الطقس الخارجية
   - عندما تتجاوز الطلبات الحد المسموح

3. **خطأ معاملات الإدخال** (422)
   - عندما تكون المعاملات مفقودة أو بتنسيق خاطئ

### آلية المعالجة
```python
@app.exception_handler(CityNotFoundException)
async def city_not_found_handler(request: Request, exc: CityNotFoundException):
    return JSONResponse(
        status_code=400,
        content={"error": "City not found", "message": str(exc)}
    )
```

## استراتيجية الاختبار

### اختبارات الوحدة (Unit Tests)
- اختبار كل خدمة بشكل منفصل
- محاكاة الاستجابات من الخدمات الخارجية
- اختبار حالات الأخطاء المختلفة

### اختبارات التكامل (Integration Tests)
- اختبار APIs كاملة من البداية للنهاية
- اختبار التفاعل مع الخدمات الخارجية الحقيقية (في بيئة الاختبار)

### اختبارات الأداء
- اختبار زمن الاستجابة للطلبات
- اختبار التعامل مع الطلبات المتزامنة

## التبعيات والمكتبات

### المكتبات الأساسية
- `fastapi`: إطار العمل الرئيسي
- `uvicorn`: خادم ASGI
- `pydantic`: التحقق من صحة البيانات
- `httpx`: للطلبات HTTP غير المتزامنة

### مكتبات الوقت والمناطق الزمنية
- `pytz`: للتعامل مع المناطق الزمنية
- `python-dateutil`: لمعالجة التواريخ المتقدمة

### مكتبات الاختبار
- `pytest`: إطار الاختبار
- `pytest-asyncio`: لاختبار الكود غير المتزامن
- `httpx`: لاختبار APIs

## الإعدادات والتكوين

### متغيرات البيئة
```
WEATHER_API_KEY=your_openweathermap_api_key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
LOG_LEVEL=INFO
```

### إعدادات التطبيق
```python
class Settings(BaseSettings):
    weather_api_key: str
    weather_api_url: str = "https://api.openweathermap.org/data/2.5/weather"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```