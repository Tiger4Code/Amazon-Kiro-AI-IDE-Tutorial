from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from .routers import time_router, weather_router
from .utils.exceptions import CityNotFoundException, WeatherServiceException, TimezoneNotFoundException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Time & Weather API",
    description="API للحصول على معلومات الوقت والطقس للمدن",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware لتسجيل الطلبات والاستجابات"""
    start_time = time.time()
    
    # تسجيل الطلب الوارد
    logger.info(f"📥 {request.method} {request.url.path} - Client: {request.client.host}")
    
    # معالجة الطلب
    response = await call_next(request)
    
    # حساب وقت المعالجة
    process_time = time.time() - start_time
    
    # تسجيل الاستجابة
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    # إضافة وقت المعالجة للاستجابة
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Exception handlers - معالجات الاستثناءات العامة
@app.exception_handler(CityNotFoundException)
async def city_not_found_handler(request: Request, exc: CityNotFoundException):
    """معالج استثناء المدينة غير الموجودة"""
    logger.warning(f"🏙️ City not found: {exc.city_name} - Path: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={
            "error": "city_not_found",
            "message": f"المدينة '{exc.city_name}' غير موجودة في قاعدة البيانات",
            "supported_cities_endpoint": "/weather/cities"
        }
    )

@app.exception_handler(WeatherServiceException)
async def weather_service_handler(request: Request, exc: WeatherServiceException):
    """معالج استثناء خدمة الطقس"""
    logger.error(f"🌤️ Weather service error: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=503,
        content={
            "error": "weather_service_unavailable",
            "message": f"خطأ في خدمة الطقس: {str(exc)}",
            "retry_after": "يرجى المحاولة مرة أخرى لاحقاً"
        }
    )

@app.exception_handler(TimezoneNotFoundException)
async def timezone_not_found_handler(request: Request, exc: TimezoneNotFoundException):
    """معالج استثناء المنطقة الزمنية غير الموجودة"""
    logger.error(f"🕐 Timezone error: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "timezone_error",
            "message": f"خطأ في المنطقة الزمنية: {str(exc)}",
            "supported_cities_endpoint": "/weather/cities"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """معالج الاستثناءات العامة لـ HTTP"""
    logger.warning(f"⚠️ HTTP Exception: {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """معالج الاستثناءات العامة غير المتوقعة"""
    logger.error(f"💥 Unexpected error: {str(exc)} - Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "حدث خطأ داخلي في الخادم",
            "support": "يرجى المحاولة مرة أخرى أو الاتصال بالدعم الفني"
        }
    )

# Include routers
app.include_router(time_router.router)
app.include_router(weather_router.router)

@app.get("/")
async def root():
    """نقطة دخول التطبيق - رسالة ترحيب"""
    logger.info("🏠 Root endpoint accessed")
    return {
        "message": "مرحباً بك في API الوقت والطقس",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "time_comparison": "/time/comparison?city1=Cairo&city2=London",
            "weather": "/weather/?city=Cairo",
            "supported_cities": "/weather/cities",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "مقارنة الأوقات بين المدن",
            "معلومات الطقس الحالية",
            "دعم المدن العربية والعالمية",
            "توثيق تفاعلي"
        ]
    }

@app.get("/health")
async def health_check():
    """فحص صحة التطبيق"""
    logger.info("💚 Health check accessed")
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "services": {
            "time_service": "operational",
            "weather_service": "operational"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)