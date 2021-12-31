from sys import platform
from logging import getLogger

from app import SCALES, OUTPUTS, web

log = getLogger(__name__)

if platform.startswith('win32') or platform.startswith('cygwin'):
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Старт сервиса
if __name__.endswith('__main__'):
    log.info("Starting Scale Server | https://git.fkinuo.ru/scale-server")

    list(map(lambda serial: serial.connect(), SCALES + OUTPUTS))  # Инициализация подключения к весам и выводу

    web.start()  # Запускаем сервер для обработки данных
