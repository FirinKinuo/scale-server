import ast
from sys import platform
from os import environ, path
from dotenv import load_dotenv
from serial.tools import list_ports

from app import Serial, Web

if platform.startswith('win32') or platform.startswith('cygwin'):
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def _setup_new_env_data() -> str:
    """
    Создает данные в виртуальном окружении
    :return: Путь к файлу .env
    """

    def input_env_data(message: str = "", error_count: int = 3, return_type: type = str, default=None) -> str:
        while True:
            try:
                return return_type(input(message) or default)
            except ValueError:
                error_count -= 1
                print("Ошибка ввода, попробуйте еще раз")

    env_params = {}

    print("Первый запуск, необходимо задать параметры:")

    serial_ports = list_ports.comports()
    print("Доступные ком-порты:")
    for port, desc in serial_ports:
        print(f"{port}: {desc}")

    print('---Параметры порта ввода---')
    env_params['input'] = {
        'path': input_env_data("Ком-порт: "),
        'baudrate': input_env_data("Частота опроса (9600 по-умолчанию): ", default=9600, return_type=int)
    }

    print('---Параметры портов вывода---')
    if input_env_data("Настроить порты вывода?(y/n) ").lower() in ['yes', 'y', 'д', 'да']:
        env_params['outputs'] = []
        for port_iter in range(0, int(input_env_data("Количество портов вывода: "))):
            env_params['outputs'].append({
                'path': input_env_data("Ком-порт: "),
                'baudrate': input_env_data("Частота опроса (9600 по-умолчанию): ", default=9600, return_type=int)
            })

    print('---Параметры веб-сервера---')
    env_params['web'] = {
        'host': input_env_data("Хост (0.0.0.0 по-умолчанию): ", default="0.0.0.0"),
        'port': input_env_data("Порт (3000 по-умолчанию): ", default=3000, return_type=int)
    }

    with open('.env', 'w') as env_file:
        data_write = f"COMPORT_PATH={env_params['input']['path']}\n" \
                     f"COMPORT_BAUDRATE={env_params['input']['baudrate']}\n" \
                     f"WEB_PORT={env_params['web']['host']}\n" \
                     f"WEB_HOST={env_params['web']['port']}\n"

        for index, output_com in enumerate(env_params['outputs']):
            data_write += f"{index}_OUTPUT_COMPORT_DATA={output_com}\n"

        env_file.write(data_write)

    return path.join(path.dirname(__file__), '.env')


def _load_env_data() -> None:
    """
    Запись переменных окружения из .env в окружение python
    :return:
    """
    dotenv_path = path.join(path.dirname(__file__), '.env')
    if path.exists(dotenv_path):
        if input("Изменить настройки?(y/n) ").lower() in ['yes', 'y', 'д', 'да']:
            load_dotenv(_setup_new_env_data())
        else:
            load_dotenv(dotenv_path)
    else:
        load_dotenv(_setup_new_env_data())


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
if __name__.endswith('__main__'):
    _load_env_data()

    com_serial = _init_comport()

    # Создаем экземпляр класса для работы c Web
    web = Web(serial=com_serial, host=environ.get('WEB_HOST'), port=int(environ.get('WEB_PORT')))
    web.start()  # Запускаем сервер для обработки данных
