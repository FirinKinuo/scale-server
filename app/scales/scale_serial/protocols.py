from enum import Enum

from app.scales.scale_serial import midl


class SerialProtocols(Enum):
    """Перечисление протоколов связи с весами по Serial"""
    MIDL = midl.MidlScale
