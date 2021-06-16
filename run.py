from os import environ, path
from dotenv import load_dotenv

from app import Serial, Web


# Старт сервиса
if __name__ == '__main__':
    # Запись переменных окружения из .env в окружение python
    dotenv_path = path.join(path.dirname(__file__), '.env')
    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Создаем экземпляр класса COM-PORT с данными из .env
    com_serial = Serial(port=environ.get('COMPORT_PATH'), baudrate=environ.get('COMPORT_BAUDRATE'))

    # Создаем экземпляр класса для работы c Web
    web = Web(serial=com_serial, host='localhost', port=3000)
    web.start()  # Запускаем сервер для обработки данных
