import serial
import re
import asyncio
from .fpylog import Log


logger = Log(file_log=True)


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
                 timeout: float = 0, output_serial=None, direction: str = "Порт ввода"):
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

        if self.output_serial is not None:
            for com in self.output_serial:
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

    def read(self) -> [float, str]:
        """
        Метод для чтения данных из компорта, возвращает float-значение с весом
        :return: float, str: Значение веса и сырые данные | Если с com-port не приходят данные, вес 0.0 и сообщение
        """

        # Ждем получения данных
        if self.serial.in_waiting:
            # Если данные получены
            raw_weight_data = self.serial.read(self.serial.in_waiting).decode('Windows-1251')  # Читаем с декодированием
            try:
                self.data = float(re.findall("[+-]?\d+\.\d+", raw_weight_data)[0])  # Пропускаем данные через регулярку

                # Если был передан ком-порт на вывод данных, то отправляем в него данные
                if self.output_serial is not None:
                    for com in self.output_serial:
                        try:
                            com.send_board(str(self.data))
                        except AttributeError:
                            pass
            except IndexError:
                pass

            logger.info(f"{self.data}")
            return self.data
        else:
            # Если данных нет - отправляем последние данные
            logger.warn(f"{self.data}")
            return self.data

    def send_board(self, message: str) -> None:
        """
        Метод для отправки данных на табло-повторитель
        :param message: Данные для отображения на табло
        :return:
        """
        self.serial.write(b'\x81\x20\x20' + str.encode(message) + b'\x20\x20\x0D\x0A\x00')
