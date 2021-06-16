import serial
import re


class Serial:
    """
    Класс для работы с COM-PORT
    """
    EMPTY_DATA = "Отсутствуют данные с COM-PORT"
    SERIAL_CLOSED = False
    SERIAL_OPENED = True

    def __init__(self, port: str, baudrate=9600, byte_size=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                 stop_bits=serial.STOPBITS_ONE, timeout=0):
        self.port = port
        self.baudrate = baudrate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.timeout = timeout
        self.serial = None

    def start(self) -> bool:
        """
        Открывает порт и делает его доступным для чтения и записи
        :return: SERIAL_OPENED или SERIAL_CLOSE
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.byte_size,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=self.timeout
            )

            print(f"{self.serial.port} открыт")

            return self.SERIAL_OPENED

        except serial.SerialException as err:
            err_msg = err.args[0]
            print(f"Невозможно открыть порт {self.port} {err_msg[err_msg.find(':'):]}")
            return self.SERIAL_CLOSED

    def read(self) -> [float, str]:
        """
        Метод для чтения данных из компорта, возвращает float-значение с весом
        :return: float, str: Значение веса и сырые данные | Если с com-port не приходят данные, вес 0.0 и сообщение
        """

        if self.serial.in_waiting:
            raw_weight_data = self.serial.read(self.serial.in_waiting).decode('Windows-1251')
            weight_data = float(re.findall("[+-]?\d+\.\d+", raw_weight_data)[0])
            return weight_data, raw_weight_data
        else:
            return 0.0, self.EMPTY_DATA

