import ast
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


def _init_comport() -> Serial:
    """
    Инизиализация ком-портов по данным из .env
    :return: Экзмепляр класса app.Serial
    """

    # Инизиализация компорта вывода
    def init_output_com(com): return Serial(port=com.get('path'), baudrate=int(com.get('baudrate')),
                                            direction=Serial.TYPE_OUTPUT)

    # Генератор списка с классами компорта на вывод
    output_comports = [init_output_com(ast.literal_eval(environ.get(com)))
                       for com in environ.keys() if "OUTPUT_COMPORT_DATA" in com]

    return Serial(port=environ.get('COMPORT_PATH'), baudrate=int(environ.get('COMPORT_BAUDRATE')),
                  output_serial=output_comports, direction=Serial.TYPE_INPUT)


# Старт сервиса
if __name__ == '__main__':
    _load_env_data()

    com_serial = _init_comport()

    # Создаем экземпляр класса для работы c Web
    web = Web(serial=com_serial, host=environ.get('WEB_HOST'), port=int(environ.get('WEB_PORT')))
    web.start()  # Запускаем сервер для обработки данных
