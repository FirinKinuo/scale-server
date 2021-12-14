from app.scales import ScaleBase


class EthernetBase(ScaleBase):
    def __init__(self, host: str, port: int, protocol: str = 'Ethernet'):
        self.host = host
        self.port = port
        self.protocol = protocol

    def __str__(self):
        return f"Scale address: {self.host}:{self.port} | Proto: {self.protocol}"
