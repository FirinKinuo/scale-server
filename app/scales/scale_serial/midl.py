"""Пакет для работы с весами фирмы МИДЛ"""
import re

from logging import getLogger
from time import sleep

from app.scales.scale_serial.base import SerialBase
from app.scales import ScaleBase

log = getLogger(__name__)


class MidlScale(SerialBase, ScaleBase):
    """Класс для работы с весами по ком-порту"""

    def __init__(self, auto_transfer: bool, **kwargs):
        super().__init__(**kwargs)
        self.auto_transfer = auto_transfer

    def __str__(self):
        return f"Scale: {self.port} | Proto: МИДЛ"

    def _get_weight_continuous_mode(self) -> float:
        """
        Получить данные о весе в режиме непрерывной передачи данных
        Returns:
            float: Вес с точкой, полученный от терминала

        Raises:
            ValueError: Если невозможно получить данные о весе от терминала
        """
        self.serial.flushInput()
        sleep(0.12)
        if self.serial.in_waiting:
            raw_weight_data = self.serial.read(self.serial.in_waiting).decode('Windows-1251')
            try:
                self.last_weight = float(re.findall(r"(\d+\.?\d*)", raw_weight_data)[-1])
            except (AttributeError, IndexError) as err:
                log.error(err)

        return self.last_weight

    def _get_weight_command_mode(self) -> float:
        """
        Получить данные о весе в командном режиме передачи данных
        Returns:
            float: Вес с точкой, полученный от терминала

        Raises:
            ValueError: Если невозможно получить данные о весе от терминала
        """
        self.serial.write(b'\x0a')

        if self.serial.in_waiting:
            raw_weight_data = self.serial.read(self.serial.in_waiting)
            try:
                return float(''.join(str(x) for x in raw_weight_data[:-2])[::-1])
            except AttributeError as err:
                raise ValueError(f"Невозможно получить данные с весов") from err
        else:
            raise ValueError(f"Невозможно получить данные с весов")

    def get_weight(self) -> float:
        """
        Получить вес с ком-порта
        Returns:
            float: Значение веса, получаемый с ком порта
        """
        return self._get_weight_continuous_mode() if self.auto_transfer else self._get_weight_command_mode()
