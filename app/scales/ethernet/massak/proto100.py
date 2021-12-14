import socket

from typing import Any
from enum import Enum
from logging import getLogger

from app.scales.ethernet.base import EthernetBase

log = getLogger(__name__)


class ProtoConnection(EthernetBase):
    """Класс для работы с протоколом 100 компании МАССА-К"""

    class ErrorCodes(Enum):
        """Перечисление с кодами ошибок"""
        OVERLOAD_WEIGHT = 8
        NOT_WEIGHING_MODE = 9
        NO_CONNECTION_WITH_SCALES = 17
        LOAD_WHEN_ON_ENGAGED = 18
        SCALES_DEFECTIVE = 19

        @classmethod
        def has_value(cls, value: Any) -> bool:
            """
            Проверка наличия значения в перечислении
            Args:
                value (Any): Искомое значение

            Returns:
                bool: Булево значение нахождения значения в перечислении
            """
            return value in cls._value2member_map_  # pylint: disable=E1101

    class ProtocolCodes(Enum):
        """Перечисление кодов протокола"""
        WEIGHT_REQUEST = 23
        WEIGHT_RESPONSE = 24
        CMD_ERROR = 28

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connected = False
        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.connection.settimeout(1.5)

    def connect(self):
        """Инициализация подключения к терминалу"""
        try:
            connection_command = bytes.fromhex("F8 55 CE 01 00 00 00 00")
            log.info(f"Попытка подключения к {self.host}:{self.port}")
            self.connection.connect((self.host, self.port))

            # Подключение к терминалу, отправкой команды и получением 34 байта ответа
            self.connection.send(connection_command)
            self.connection.recv(34)
            self.connected = True

        except socket.timeout as err:
            raise TimeoutError(f"Невозможно подключиться к терминалу {self.host}:{self.port}") from err

    def _init_new_connection(self):
        self.connected = False
        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.connection.settimeout(1.5)

    def _send_weight_request(self) -> str:
        """
        Отправить запрос на получение веса от терминала
        Returns:
            Строка с HEX ответом от весов
        """
        if not self.connected:
            self.connect()

        response_size = 20
        get_weight_command = bytes.fromhex("F8 55 CE 01 00 23 23 00")

        try:
            self.connection.send(get_weight_command)
        except (socket.timeout, BrokenPipeError):
            log.error("Невозможно отправить управляющий сигнал, переподключение..")
            self._init_new_connection()
            return self._send_weight_request()

        raw_weight = self.connection.recv(response_size)

        return raw_weight.hex()

    @staticmethod
    def _get_command_code(command_string: str) -> int:
        """
        Получить код команды терминала
        Args:
            command_string (str): HEX строка с ответом от терминала

        Returns:
            int: Код команды терминала
        """
        return int(command_string[10:12])  # Отсекаем заголовочные байты и байты тела

    @staticmethod
    def _get_weight_division(response_string) -> float:
        """
        Получить множитель веса
        Args:
            response_string (str): HEX строка с ответом от терминала

        Returns:
            float: Множитель веса
        """
        # Список со значениями множителя веса, получаемых от терминала
        weight_division = [
            0.1,
            1,
            10,
            100,
            1000
        ]

        return weight_division[int(response_string[20:22])]

    @staticmethod
    def _parse_weight(response_string: str) -> int:
        """
        Парсинг веса из HEX-строки ответа
        Args:
            response_string (str): HEX строка с ответом от терминала

        Returns:
            int: Полученный вес после парсинга
        """
        weight_bytes = response_string[12:20]  # Отсекаем все байты, помимо байтчов тела
        return (
                int(weight_bytes[0:2], 16) * 0x01 +
                int(weight_bytes[2:4], 16) * 0x100 +
                int(weight_bytes[4:6], 16) * 0x10000 +
                int(weight_bytes[6:8], 16) * 0x1000000
        )

    @staticmethod
    def _get_error_code(command_string: str):
        """
        Получить код ошибки терминала
        Args:
            command_string (str): HEX строка с ответом от терминала

        Returns:
            int: Код ошибки терминала
        """
        return int(command_string[12:14])  # Отсекаем все байты, помимо байтов тела

    @classmethod
    def _handle_error(cls, command_string: str):
        """
        Обработчик ошибок
        Args:
            command_string:

        Raises:
            ConnectionError: Ошибка

        """
        error_code = cls._get_error_code(command_string=command_string)
        error = cls.ErrorCodes(error_code).name if cls.ErrorCodes.has_value(
            error_code) else f"Unknown Error ID: 0x{error_code}"

        raise ConnectionError(error)

    def get_weight(self) -> float:  # pylint: disable=R1710
        """
        Получить вес от терминала весов

        Returns:
            float: Итоговый вес от терминала

        Raises:
            ConnectionError: Ошибка выполнения команды
        """
        weight_response = self._send_weight_request()
        response_code = self._get_command_code(command_string=weight_response)

        if response_code == self.ProtocolCodes.CMD_ERROR.value:
            self._handle_error(command_string=weight_response)

        elif response_code == self.ProtocolCodes.WEIGHT_RESPONSE.value:
            weight = self._parse_weight(response_string=weight_response)
            division = self._get_weight_division(response_string=weight_response)

            return weight * division
