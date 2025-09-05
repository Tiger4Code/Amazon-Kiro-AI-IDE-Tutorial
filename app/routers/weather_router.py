from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from ..services.weather_service import weather_service
from ..models.weather_models import WeatherResponse
from ..utils.exceptions import CityNotFoundException, WeatherServiceException

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "المدينة غير موجودة"}}
)


@router.get("/", response_model=WeatherResponse)
async def get_weather(
    city: Annotated[str, Query(
        description="اسم المدينة للحصول على معلومات الطقس",
        example="القاهرة"
    )]
) -> WeatherResponse:
    """
    الحصول على معلومات الطقس الحالية لمدينة معينة
    
    - **city**: اسم المدينة (يمكن أن يكون بالعربية أو الإنجليزية)
    
    يدعم المدن التالية:
    - القاهرة / Cairo
    - الرياض / Riyadh  
    - لندن / London
    """
    # التحقق من صحة معامل المدينة
    if not city or not city.strip():
        raise HTTPException(
            status_code=400,
            detail="يجب تحديد اسم المدينة"
        )
    
    try:
        
        # الحصول على معلومات الطقس
        weather_info = await weather_service.get_weather(city.strip())
        return weather_info
        
    except CityNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=f"المدينة '{city}' غير موجودة في قاعدة البيانات"
        )
    except WeatherServiceException as e:
        raise HTTPException(
            status_code=503,
            detail=f"خطأ في خدمة الطقس: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="حدث خطأ داخلي في الخادم"
        )


@router.get("/cities", response_model=dict)
async def get_supported_cities():
    """
    الحصول على قائمة المدن المدعومة
    """
    return {
        "supported_cities": [
            {"arabic": "القاهرة", "english": "Cairo"},
            {"arabic": "الرياض", "english": "Riyadh"},
            {"arabic": "لندن", "english": "London"}
        ],
        "message": "يمكنك استخدام الأسماء العربية أو الإنجليزية للمدن"
    }