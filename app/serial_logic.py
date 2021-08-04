import serial
import re
import asyncio
from .fpylog import Log

logger = Log(file_log=False)


class Serial:
    """
    Класс для работы с COM-PORT
    """
    EMPTY_DATA = "Отсутствуют данные с COM-PORT"
    TYPE_INPUT = "Порт ввода"
    TYPE_OUTPUT = "Порт вывода"
    SERIAL_CLOSED = False
    SERIAL_OPENED = True

    def __init__(self, port: str, baudrate: int = 9600,
                 byte_size=serial.EIGHTBITS, parity=serial.PARITY_NONE, stop_bits=serial.STOPBITS_ONE,
                 timeout: float = 0, output_serial=None, direction: str = "Порт ввода", auto_transfer: bool = True):
        self.port = port
        self.baudrate = baudrate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.timeout = timeout
        self.data = 0.0
        self.serial = None
        self.output_serial = output_serial
        self.direction = direction
        self.auto_transfer = auto_transfer

        if self.output_serial is not None:
            for com in self.output_serial:
                if com.serial is None:
                    com.start()

    async def background_reading(self):
        while True:
            self.read()
            await asyncio.sleep(0.3)

    def start(self) -> bool:
        """
        Открывает порт и делает его доступным для чтения и записи
        :return: SERIAL_OPENED или SERIAL_CLOSE
        """
        logger.info(f"Попытка открыть {self.port} - {self.baudrate} Бод | {self.direction}")
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.byte_size,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=self.timeout
            )

            logger.success(f"Открыт {self.serial.port}")

            return self.SERIAL_OPENED

        except serial.SerialException as err:
            logger.error(f"Невозможно открыть порт {self.port} {err}")
            return self.SERIAL_CLOSED

    def read(self) -> [int, str]:
        """
        Метод для чтения данных из компорта, возвращает int-значение веса в КГ
        :return: int, str: Значение веса и сырые данные | Если с com-port не приходят данные, вес 0.0 и сообщение
        """

        # Ждем получения данных
        try:
            if not self.auto_transfer:
                self.serial.write(b'\x0a')

            if self.serial.in_waiting:
                # Если данные получены
                raw_weight_data = self.serial.read(self.serial.in_waiting)  # Читаем с декодированием
                try:
                    self.data = int(
                        re.findall("[+-]?\d+\.\d+", raw_weight_data.decode('Windows-1251'))[
                            0]) * 1000 if self.auto_transfer else int(
                        ''.join(str(x) for x in raw_weight_data[:-2])[::-1])  # Пропускаем данные через регулярку

                    # Если был передан ком-порт на вывод данных, то отправляем в него данные
                    if self.output_serial is not None:
                        for com in self.output_serial:
                            try:
                                com.send_board(str(self.data))
                            except AttributeError:
                                pass
                except IndexError:
                    pass

                return self.data
            else:
                return self.data

        except AttributeError:
            logger.error(f"Не получается открыть порт ввода, проверьте настройки")

    def send_board(self, message: str) -> None:
        """
        Метод для отправки данных на табло-повторитель
        :param message: Данные для отображения на табло
        :return:
        """
        self.serial.write(b'\x81\x20\x20' + str.encode(f"{int(message):05}") + b'\x20\x20\x0d\x0A')
