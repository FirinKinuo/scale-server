from logging import getLogger

import serial as pyserial

logger = getLogger(__name__)


class SerialBase:
    """Класс для работы с COM-PORT на выводящие устройства"""

    def __init__(self, port: str, baudrate: int = 9600, byte_size=8, parity='n', stop_bits=1, protocol: str = 'Serial',
                 timeout: float = 0):
        self.port = port
        self.baudrate = baudrate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.timeout = timeout
        self.serial = None
        self.protocol = protocol

    def connect(self):
        """Открывает порт и делает его доступным для чтения и записи"""
        try:
            self.serial = pyserial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.byte_size,
                parity=self.parity,
                stopbits=self.stop_bits,
                timeout=self.timeout
            )
        except pyserial.SerialException as err:
            raise SystemError(err) from err
