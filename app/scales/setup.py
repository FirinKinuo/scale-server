from app.settings import config
from app.scales import ScaleBase
from app.scales.scale_serial.protocols import SerialProtocols
from app.scales.scale_serial.output import SerialOutput
from app.scales.ethernet import EthernetProtocols


def init_scales() -> list[ScaleBase]:
    """
    Инициализация подключения к весам
    Returns:
        list[ScaleBase]:
    """
    return [SerialProtocols[scale.get('protocol').upper()].value(**scale) if 'host' not in scale else
            EthernetProtocols[scale.get('protocol').upper()].value(**scale) for scale in config.SCALES_SERIALS]


def init_output() -> list[SerialOutput]:
    """
    Инициализация подключения к устройствам вывода
    Returns:
        list[SerialOutput]:
    """
    return [SerialOutput(**output) for output in config.OUTPUT_SERIALS]
