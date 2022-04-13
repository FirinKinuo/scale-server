from typing import Callable
from contextlib import contextmanager

from app.scales.percent import get_weight_percent


class ScaleBase:
    """Базовый класс, описывающий все классы для работы с весами"""
    def __init__(self, protocol: str, weight_multiplier: float = 1.0, decimal_digits=3):
        self.connected = False
        self.protocol = protocol
        self.weight_multiplier = weight_multiplier
        self.decimal_digits = decimal_digits
        self.last_weight = 0

    def connect(self):
        """Макет метода для подключения к весам"""
        pass

    def disconnect(self):
        """Макет метода для отключения от весов"""
        pass

    def get_weight(self) -> float:
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

    @contextmanager
    def one_time_connect(self, func: Callable) -> Callable:
        """
        Контекстный менеджер для создания одноразового соединения
        Args:
            func: Callable: Метод, который должен быть выполнен в контексте

        Returns:
            Callable: Метод в контексте
        """
        try:
            if not self.connected:
                self.connect()

            yield func

        finally:
            self.disconnect()

    def get_weight_one_time_connect(self) -> float:
        """Получить значение веса в контексте одноразового соединения"""
        with self.one_time_connect(func=self.get_weight) as get_weight:
            return get_weight()
