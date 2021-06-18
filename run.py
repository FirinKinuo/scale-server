from os import environ, path
from dotenv import load_dotenv

from app import Serial, Web


def _load_env_data() -> None:
    """
    Запись переменных окружения из .env в окружение python
    :return:
    """
    dotenv_path = path.join(path.dirname(__file__), '.env')
    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)


# Старт сервиса
if __name__ == '__main__':
    _load_env_data()

    # Создаем экземпляр класса COM-PORT с данными из .env
    print(f"Попытка открыть {environ.get('COMPORT_PATH')} {environ.get('COMPORT_BAUDRATE')}бод")
    com_serial = Serial(port=environ.get('COMPORT_PATH'), baudrate=environ.get('COMPORT_BAUDRATE'))

    # Создаем экземпляр класса для работы c Web
    web = Web(serial=com_serial, host=environ.get('WEB_HOST'), port=int(environ.get('WEB_PORT')))
    web.start()  # Запускаем сервер для обработки данных
