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
    log.info("Starting...")
    print(f"Starting Scale Server || "
          f"transmission: {web.config.TRANSMISSION_HOST}:{web.config.TRANSMISSION_PORT} | "
          f"visual: {web.config.VISUAL_HOST}:{web.config.VISUAL_PORT}")

    list(map(lambda serial: serial.connect(), SCALES + OUTPUTS))  # Инициализация подключения к весам и выводу

    web.start()  # Запускаем сервер для обработки данных
