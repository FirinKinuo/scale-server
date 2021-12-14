from enum import Enum

from app.scales.ethernet import mera


class EthernetProtocols(Enum):
    """Перечисление протоколов связи с весами по Ethernet"""
    MERA = mera.MeraRequest
