from enum import Enum

from app.scales.ethernet import mera
from app.scales.ethernet.massak import proto100


class EthernetProtocols(Enum):
    """Перечисление протоколов связи с весами по Ethernet"""
    PROTO100 = proto100.ProtoConnection
    MERA = mera.MeraRequest
