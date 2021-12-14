from enum import Enum

from app.scales.ethernet import proto100, mera


class EthernetProtocols(Enum):
    """Перечисление протоколов связи с весами по Ethernet"""
    PROTO100 = proto100.ProtoConnection
    MERA = mera.MeraRequest
