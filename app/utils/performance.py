"""
وحدة تحسين الأداء والمراقبة
"""
import time
import asyncio
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


def performance_monitor(func_name: str = None):
    """
    Decorator لمراقبة أداء الوظائف
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            name = func_name or func.__name__
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > 1.0:  # تحذير إذا كان الوقت أكثر من ثانية
                    logger.warning(f"⚠️ Slow function: {name} took {execution_time:.3f}s")
                else:
                    logger.debug(f"✅ Function: {name} completed in {execution_time:.3f}s")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"❌ Function: {name} failed after {execution_time:.3f}s - Error: {str(e)}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            name = func_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > 0.5:  # تحذير إذا كان الوقت أكثر من نصف ثانية
                    logger.warning(f"⚠️ Slow function: {name} took {execution_time:.3f}s")
                else:
                    logger.debug(f"✅ Function: {name} completed in {execution_time:.3f}s")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"❌ Function: {name} failed after {execution_time:.3f}s - Error: {str(e)}")
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


class PerformanceMetrics:
    """
    فئة لجمع وتتبع مقاييس الأداء
    """
    
    def __init__(self):
        self.request_count = 0
        self.total_response_time = 0.0
        self.error_count = 0
        self.start_time = time.time()
    
    def record_request(self, response_time: float, is_error: bool = False):
        """تسجيل طلب جديد"""
        self.request_count += 1
        self.total_response_time += response_time
        
        if is_error:
            self.error_count += 1
    
    def get_average_response_time(self) -> float:
        """الحصول على متوسط وقت الاستجابة"""
        if self.request_count == 0:
            return 0.0
        return self.total_response_time / self.request_count
    
    def get_error_rate(self) -> float:
        """الحصول على معدل الأخطاء"""
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100
    
    def get_requests_per_second(self) -> float:
        """الحصول على عدد الطلبات في الثانية"""
        uptime = time.time() - self.start_time
        if uptime == 0:
            return 0.0
        return self.request_count / uptime
    
    def get_metrics_summary(self) -> dict:
        """الحصول على ملخص المقاييس"""
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "average_response_time": round(self.get_average_response_time(), 3),
            "error_rate_percentage": round(self.get_error_rate(), 2),
            "requests_per_second": round(self.get_requests_per_second(), 2),
            "uptime_seconds": round(time.time() - self.start_time, 2)
        }


# مثيل عام لمقاييس الأداء
performance_metrics = PerformanceMetrics()


def timeout_handler(timeout_seconds: float = 5.0):
    """
    Decorator لإضافة timeout للوظائف غير المتزامنة
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs), 
                    timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                logger.error(f"⏰ Function {func.__name__} timed out after {timeout_seconds}s")
                raise TimeoutError(f"Operation timed out after {timeout_seconds} seconds")
        
        return wrapper
    
    return decorator


def cache_result(ttl_seconds: int = 300):
    """
    Decorator بسيط للتخزين المؤقت (Cache)
    """
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            # إنشاء مفتاح التخزين المؤقت
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            current_time = time.time()
            
            # التحقق من وجود النتيجة في التخزين المؤقت
            if cache_key in cache:
                cached_result, cached_time = cache[cache_key]
                if current_time - cached_time < ttl_seconds:
                    logger.debug(f"🎯 Cache hit for {func.__name__}")
                    return cached_result
            
            # تنفيذ الوظيفة وحفظ النتيجة
            result = await func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            
            # تنظيف التخزين المؤقت من النتائج المنتهية الصلاحية
            expired_keys = [
                key for key, (_, cached_time) in cache.items()
                if current_time - cached_time >= ttl_seconds
            ]
            for key in expired_keys:
                del cache[key]
            
            logger.debug(f"💾 Cached result for {func.__name__}")
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            # نفس المنطق للوظائف المتزامنة
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            current_time = time.time()
            
            if cache_key in cache:
                cached_result, cached_time = cache[cache_key]
                if current_time - cached_time < ttl_seconds:
                    logger.debug(f"🎯 Cache hit for {func.__name__}")
                    return cached_result
            
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            
            # تنظيف التخزين المؤقت
            expired_keys = [
                key for key, (_, cached_time) in cache.items()
                if current_time - cached_time >= ttl_seconds
            ]
            for key in expired_keys:
                del cache[key]
            
            logger.debug(f"💾 Cached result for {func.__name__}")
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator