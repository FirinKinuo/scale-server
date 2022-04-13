from logging import getLogger
from typing import Union

import serial as pyserial

from app.scales import ScaleBase

logger = getLogger(__name__)


class SerialBase(ScaleBase):
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
        self.serial: Union[pyserial.Serial, None] = None

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

            self.connected = True

        except pyserial.SerialException as err:
            raise SystemError(err) from err

    def disconnect(self):
        self.serial.close()
        self.connected = False
