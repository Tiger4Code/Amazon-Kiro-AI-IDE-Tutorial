from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..services.time_service import time_service
from ..models.time_models import TimeComparisonResponse
from ..utils.exceptions import CityNotFoundException, TimezoneNotFoundException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/time",
    tags=["Time APIs"],
    responses={
        400: {"description": "مدينة غير موجودة"},
        422: {"description": "معاملات غير صحيحة"},
        500: {"description": "خطأ داخلي في الخادم"}
    }
)


@router.get(
    "/comparison",
    response_model=TimeComparisonResponse,
    summary="مقارنة الأوقات بين مدينتين",
    description="الحصول على الوقت الحالي في مدينتين وحساب فرق التوقيت بينهما"
)
async def compare_times(
    city1: str = Query(
        ..., 
        description="اسم المدينة الأولى",
        example="Cairo"
    ),
    city2: str = Query(
        ..., 
        description="اسم المدينة الثانية", 
        example="London"
    )
):
    """
    مقارنة الأوقات بين مدينتين
    
    - **city1**: اسم المدينة الأولى (مطلوب)
    - **city2**: اسم المدينة الثانية (مطلوب)
    
    يرجع الوقت الحالي في كلا المدينتين مع فرق التوقيت بالساعات
    """
    try:
        logger.info(f"طلب مقارنة الأوقات بين {city1} و {city2}")
        
        # التحقق من صحة المعاملات
        if not city1 or not city1.strip():
            raise HTTPException(
                status_code=422,
                detail="اسم المدينة الأولى مطلوب"
            )
        
        if not city2 or not city2.strip():
            raise HTTPException(
                status_code=422,
                detail="اسم المدينة الثانية مطلوب"
            )
        
        # الحصول على مقارنة الأوقات
        result = time_service.calculate_time_difference(
            city1.strip(), 
            city2.strip()
        )
        
        logger.info(f"تم الحصول على مقارنة الأوقات بنجاح لـ {city1} و {city2}")
        return result
        
    except CityNotFoundException as e:
        logger.warning(f"مدينة غير موجودة: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "City not found",
                "message": f"لم يتم العثور على المدينة '{str(e)}'. جرب اسم مدينة مختلف أو تأكد من الإملاء.",
                "note": "يمكنك استخدام أي مدينة في العالم! جرب: طوكيو، برلين، مكة، إسطنبول، نيودلهي، إلخ...",
                "examples": [
                    "Cairo", "القاهرة", "Tokyo", "طوكيو", 
                    "Berlin", "برلين", "Istanbul", "إسطنبول",
                    "New Delhi", "نيودلهي", "Mecca", "مكة"
                ]
            }
        )
    
    except TimezoneNotFoundException as e:
        logger.error(f"خطأ في المنطقة الزمنية: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Timezone error",
                "message": str(e)
            }
        )
    
    except Exception as e:
        logger.error(f"خطأ غير متوقع في مقارنة الأوقات: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "حدث خطأ غير متوقع، يرجى المحاولة مرة أخرى"
            }
        )