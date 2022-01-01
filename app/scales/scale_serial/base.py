from logging import getLogger

import serial as pyserial

logger = getLogger(__name__)


class SerialBase:
    """Базовый класс для работы с устройствами по comport"""

    def __init__(self,
                 port: str,
                 baudrate: int = 9600,
                 byte_size: int = 8,
                 parity: str = 'n',
                 stop_bits: int = 1,
                 timeout: float = 0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.port = port
        self.baudrate = baudrate
        self.byte_size = byte_size
        self.parity = parity
        self.stop_bits = stop_bits
        self.timeout = timeout
        self.serial = None

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
