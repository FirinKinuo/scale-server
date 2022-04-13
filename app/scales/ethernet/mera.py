from logging import getLogger

import requests

from app.scales.ethernet import EthernetBase

log = getLogger(__name__)


class MeraRequest(EthernetBase):
    """Класс для работы с сетевым протоколом МЕРА"""
    def get_weight(self) -> float:
        """
        Получить вес от терминала весов

        Returns:
            float: Итоговый вес от терминала

        Raises:
            TimeoutError: Если невозможно подключиться к указанному терминалу
        """
        try:
            weight_request = requests.get(f"http://{self.host}:{self.port}/weight.html", timeout=2.5).text
            return float(weight_request or 0)  # Когда вес равняется 0, то приходит пустая строка
        except requests.ConnectTimeout as err:
            raise TimeoutError(f"Невозможно подключиться к терминалу {self.host}:{self.port}") from err
