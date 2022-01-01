from app.scales.percent import get_weight_percent


class ScaleBase:
    """Базовый класс, описывающий все классы для работы с весами"""
    def __init__(self, protocol: str, weight_multiplier: float = 1.0):
        self.protocol = protocol
        self.weight_multiplier = weight_multiplier
        self.last_weight = 0

    def connect(self):
        """Макет метода для подключения к весам"""
        pass

    def get_weight(self):
        """Макет метода для получения данных с весов"""
        pass

    @classmethod
    def subtract_percent(cls, weight: int) -> float:
        """
        Добавить процент к весу
        Args:
            weight (int): Вес, к которому необходимо добавить вес

        Returns:
            float - Вес с процентом
        """
        weight_percent = get_weight_percent()
        return weight / 100 * (100 - weight_percent)
