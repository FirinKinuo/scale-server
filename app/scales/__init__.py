from app.scales.percent import get_weight_percent


class ScaleBase:
    """Базовый класс, описывающий все классы для работы с весами"""

    def connect(self):
        """Макет метода для подключения к весам"""
        pass

    def get_weight(self):
        """Макет метода для получения данных с весов"""
        pass

    @classmethod
    def subtract_percent(cls, weight: int):
        weight_percent = get_weight_percent()
        return weight / 100 * (100 - weight_percent)
