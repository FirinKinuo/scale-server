from app.scales import ScaleBase


class EthernetBase(ScaleBase):
    """Базовый класс для работы с весами через протоколы TCP"""
    def __init__(self, host: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = host
        self.port = port

    def __str__(self):
        return f"Scale address: {self.host}:{self.port} | Proto: {self.protocol}"
