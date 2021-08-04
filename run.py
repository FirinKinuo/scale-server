import ast
from sys import platform
from sys import path as sys_path
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
    :return: Путь к файлу config.env
    """

    def input_env_data(message: str = "", error_count: int = 3, return_type: type = str, default=None) -> [str, int]:
        while True:
            try:
                return return_type(input(message) or default)
            except ValueError:
                error_count -= 1
                print("Ошибка ввода, попробуйте еще раз")

    env_params = {}

    print("~~~~~Первый запуск, необходимо задать параметры~~~~~\n"
          "--Вносите данные внимательно\n"
          "--Для систем Windows указывается COM*\n"
          "--Для систем Linux указывается полный путь /dev/ttyS*\n"
          "--Данные по-умолчанию вносятся простым нажатием на Enter\n")

    serial_ports = list_ports.comports()
    print("---Доступные ком-порты:")
    for port in serial_ports:
        print(f"{port.description}")

    print('\n---Параметры порта ввода---')
    env_params['inputs'] = [{
        'path': input_env_data("Ком-порт: "),
        'baudrate': input_env_data("Частота опроса (9600 по-умолчанию): ", default=9600, return_type=int)
    } for _ in range(0, input_env_data("Количество портов ввода: ", return_type=int, default=0))]

    print('---Параметры портов вывода---')
    if input_env_data("Настроить порты вывода?(y/n) ").lower() in ['yes', 'y', 'д', 'да']:
        env_params['outputs'] = [{
            'path': input_env_data("Ком-порт: "),
            'baudrate': input_env_data("Частота опроса (9600 по-умолчанию): ", default=9600, return_type=int),
            'auto-transfer': input_env_data("Данные передаются автоматически?", default=True, return_type=bool)
        } for _ in range(0, input_env_data("Количество портов вывода: ", return_type=int, default=0))]

    print('---Параметры веб-сервера---')
    env_params['web'] = {
        'host': input_env_data("Хост (0.0.0.0 по-умолчанию): ", default="0.0.0.0"),
        'port': input_env_data("Порт (3000 по-умолчанию): ", default=3000, return_type=int)
    }

    with open('config.env', 'w') as env_file:
        data_write = f"WEB_PORT={env_params['web']['port']}\n" \
                     f"WEB_HOST={env_params['web']['host']}\n"

        data_write += f"INPUT_COM={env_params['inputs']}\n"
        data_write += f"OUTPUT_COM={env_params['outputs']}\n"

        env_file.write(data_write)

    return path.join(sys_path[0], 'config.env')


def _load_env_data() -> None:
    """
    Запись переменных окружения из config.env в окружение python
    :return:
    """
    dotenv_path = path.join(sys_path[0], 'config.env')
    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        load_dotenv(_setup_new_env_data())


def _init_comports() -> list:
    """
    Инизиализация ком-портов по данным из config.env
    :return: Экзмепляр класса app.Serial
    """

    # Инизиализация компорта вывода
    def init_output_com(com): return Serial(port=com.get('path'), baudrate=int(com.get('baudrate')),
                                            direction=Serial.TYPE_OUTPUT)

    def init_input_com(com, output_com): return Serial(port=com.get('path'), baudrate=int(com.get('baudrate')),
                                                       output_serial=output_com, direction=Serial.TYPE_OUTPUT,
                                                       auto_transfer=com.get('auto-transfer'))

    # Генератор списка с классами компорта на вывод
    output_comports = [init_output_com(com) for com in ast.literal_eval(environ.get('OUTPUT_COM'))]

    return [init_input_com(com, output_comports) for com in ast.literal_eval(environ.get('INPUT_COM'))]


# Старт сервиса
if __name__.endswith('__main__'):
    """
    Если это читает тот, кому придется что-то допиливать в этом коде,
    Знай, 1С-ники - плохие люди, которые пилят ебанные костыли,
    Из-за которых нормальный код приходится переделывать в какое-то уебище..
    Лишь бы со стороны 1С не было ебанных проблем..
    """
    print("Weight ComPort v1.3.1 | https://github.com/FirinKinuo")
    _load_env_data()

    com_serial_list = _init_comports()

    # Создаем экземпляр класса для работы c Web
    web = Web(serial_list=com_serial_list, host=environ.get('WEB_HOST'), port=int(environ.get('WEB_PORT')))
    web.start()  # Запускаем сервер для обработки данных
