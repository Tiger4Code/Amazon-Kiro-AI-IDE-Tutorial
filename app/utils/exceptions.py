class CityNotFoundException(Exception):
    """استثناء عندما لا يتم العثور على المدينة"""
    def __init__(self, city_name: str):
        self.city_name = city_name
        super().__init__(f"المدينة '{city_name}' غير موجودة أو غير مدعومة")


class WeatherServiceException(Exception):
    """استثناء عندما تفشل خدمة الطقس الخارجية"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"خطأ في خدمة الطقس: {message}")


class TimezoneNotFoundException(Exception):
    """استثناء عندما لا يتم العثور على المنطقة الزمنية للمدينة"""
    def __init__(self, city_name: str):
        self.city_name = city_name
        super().__init__(f"لا يمكن تحديد المنطقة الزمنية للمدينة '{city_name}'")