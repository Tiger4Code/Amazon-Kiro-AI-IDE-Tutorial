# Time & Weather API

API للحصول على معلومات الوقت والطقس للمدن المختلفة باستخدام FastAPI.

## المميزات

- 🕐 **مقارنة الأوقات**: مقارنة الوقت الحالي بين مدينتين مختلفتين
- 🌤️ **معلومات الطقس**: الحصول على معلومات الطقس الحالية لأي مدينة
- 🌍 **دعم المدن العربية والعالمية**: يدعم أسماء المدن بالعربية والإنجليزية
- 📱 **واجهة تفاعلية**: توثيق تفاعلي باستخدام Swagger UI
- ✅ **اختبارات شاملة**: مجموعة كاملة من الاختبارات الآلية

## المدن المدعومة

### مدن عربية:
- القاهرة / Cairo
- الرياض / Riyadh  
- دبي / Dubai
- بيروت / Beirut
- بغداد / Baghdad
- دمشق / Damascus
- عمان / Amman

### مدن عالمية:
- لندن / London
- باريس / Paris
- نيويورك / New York
- طوكيو / Tokyo
- موسكو / Moscow
- سيدني / Sydney

## التثبيت والإعداد

### المتطلبات الأساسية
- Python 3.8+
- pip

### خطوات التثبيت

1. **استنساخ المشروع**
```bash
git clone <repository-url>
cd fastapi-time-weather
```

2. **إنشاء وتفعيل البيئة الافتراضية** ⚠️ **مهم جداً**
```bash
# إنشاء البيئة الافتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على macOS/Linux:
source venv/bin/activate

# على Windows:
venv\Scripts\activate
```

3. **تثبيت التبعيات**
```bash
pip install -r requirements.txt
```

4. **إعداد متغيرات البيئة**
```bash
# نسخ ملف البيئة
cp .env.example .env

# تحرير الملف وإضافة مفتاح API للطقس (اختياري)
# WEATHER_API_KEY=your_openweathermap_api_key
# WEATHER_API_URL=http://api.openweathermap.org/data/2.5/weather
```

## تشغيل التطبيق

### تشغيل الخادم المحلي
```bash
uvicorn app.main:app --reload
```

الخادم سيعمل على: `http://127.0.0.1:8000`

### الوصول للتوثيق التفاعلي
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## استخدام API

### 1. مقارنة الأوقات بين مدينتين

**Endpoint**: `GET /time/comparison`

**المعاملات**:
- `city1`: اسم المدينة الأولى
- `city2`: اسم المدينة الثانية

**مثال**:
```bash
curl "http://127.0.0.1:8000/time/comparison?city1=القاهرة&city2=لندن"
```

**الاستجابة**:
```json
{
  "city1": "القاهرة",
  "city1_time": "2024-01-15T14:30:00",
  "city1_timezone": "Africa/Cairo",
  "city2": "لندن", 
  "city2_time": "2024-01-15T12:30:00",
  "city2_timezone": "Europe/London",
  "time_difference_hours": 2.0
}
```

### 2. الحصول على معلومات الطقس

**Endpoint**: `GET /weather/`

**المعاملات**:
- `city`: اسم المدينة

**مثال**:
```bash
curl "http://127.0.0.1:8000/weather/?city=الرياض"
```

**الاستجابة**:
```json
{
  "city": "Riyadh",
  "temperature": 35.2,
  "description": "سماء صافية",
  "humidity": 25,
  "feels_like": 38.5
}
```

### 3. قائمة المدن المدعومة

**Endpoint**: `GET /weather/cities`

**مثال**:
```bash
curl "http://127.0.0.1:8000/weather/cities"
```

## تشغيل الاختبارات

### تشغيل جميع الاختبارات
```bash
pytest
```

### تشغيل اختبارات محددة
```bash
# اختبارات خدمة الوقت
pytest tests/test_time_service.py -v

# اختبارات خدمة الطقس  
pytest tests/test_weather_service.py -v

# اختبارات API الوقت
pytest tests/test_time_api.py -v

# اختبارات API الطقس
pytest tests/test_weather_api.py -v
```

### تشغيل الاختبارات مع تقرير التغطية
```bash
pytest --cov=app tests/
```

## هيكل المشروع

```
fastapi-time-weather/
├── app/
│   ├── __init__.py
│   ├── main.py                 # نقطة دخول التطبيق
│   ├── models/
│   │   ├── __init__.py
│   │   ├── time_models.py      # نماذج بيانات الوقت
│   │   └── weather_models.py   # نماذج بيانات الطقس
│   ├── services/
│   │   ├── __init__.py
│   │   ├── time_service.py     # خدمة الوقت والمناطق الزمنية
│   │   └── weather_service.py  # خدمة الطقس
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── time_router.py      # مسارات API للوقت
│   │   └── weather_router.py   # مسارات API للطقس
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # إعدادات التطبيق
│       └── exceptions.py       # الاستثناءات المخصصة
├── tests/
│   ├── __init__.py
│   ├── test_time_service.py    # اختبارات خدمة الوقت
│   ├── test_weather_service.py # اختبارات خدمة الطقس
│   ├── test_time_api.py        # اختبارات API الوقت
│   └── test_weather_api.py     # اختبارات API الطقس
├── venv/                       # البيئة الافتراضية
├── .env                        # متغيرات البيئة
├── requirements.txt            # التبعيات
└── README.md                   # هذا الملف
```

## التبعيات الرئيسية

- **FastAPI**: إطار عمل الويب السريع
- **Uvicorn**: خادم ASGI
- **Pydantic**: التحقق من صحة البيانات
- **httpx**: عميل HTTP غير متزامن
- **pytz**: التعامل مع المناطق الزمنية
- **pytest**: إطار عمل الاختبارات

## معالجة الأخطاء

التطبيق يتعامل مع الأخطاء التالية:

- **404**: المدينة غير موجودة
- **400**: معاملات غير صحيحة
- **503**: خطأ في خدمة الطقس الخارجية
- **500**: خطأ داخلي في الخادم

## ملاحظات مهمة

### ⚠️ البيئة الافتراضية
**يجب دائماً تفعيل البيئة الافتراضية قبل تثبيت أي حزم أو تشغيل التطبيق**

```bash
# تفعيل البيئة الافتراضية
source venv/bin/activate  # macOS/Linux
# أو
venv\Scripts\activate     # Windows
```

### 🔑 مفتاح API للطقس
حالياً التطبيق يستخدم بيانات ثابتة للطقس. لاستخدام بيانات حقيقية:

1. احصل على مفتاح API من [OpenWeatherMap](https://openweathermap.org/api)
2. أضف المفتاح في ملف `.env`:
```
WEATHER_API_KEY=your_api_key_here
```

## المساهمة

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## الدعم

إذا واجهت أي مشاكل أو لديك أسئلة، يرجى فتح [issue](../../issues) في المستودع.