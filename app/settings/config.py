import sys
import logging

from pathlib import Path

import yaml

EXTERNAL_FILES_DIR = Path('/etc', 'scale-server')
YAML_CONFIG_PATH = Path(EXTERNAL_FILES_DIR, 'config.yaml')
PERCENT_SAVE_PATH = Path(EXTERNAL_FILES_DIR, 'percent.tmp')
IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # Если найдены пути тестов, то переходим в режим теста


def get_config_from_yaml() -> dict:
    """
    Получение конфигурации из файла .yaml

    Returns:
        (dict): Словарь с конфигурацией из .yaml файла
    """
    try:
        with open(YAML_CONFIG_PATH, 'r', encoding="utf-8") as config_file:
            return yaml.load(stream=config_file, Loader=yaml.loader.SafeLoader)
    except FileNotFoundError as err:
        YAML_CONFIG_PATH.parent.mkdir(parents=True)
        YAML_CONFIG_PATH.touch()
        raise SystemExit(f"Проверьте файл конфигурации! Путь: {YAML_CONFIG_PATH}") from err


_config = get_config_from_yaml()

DEBUG = _config.get('debug') or False
USE_PERCENT = _config.get('use_percent') or False
LOGGER_LEVEL = logging.getLevelName(_config.get('log_level').upper())

TRANSMISSION_HOST = _config.get('web').get('transmission').get('host') or 'localhost'
TRANSMISSION_PORT = _config.get('web').get('transmission').get('port') or 3000
VISUAL_HOST = _config.get('web').get('visual').get('host') or 'localhost'
VISUAL_PORT = _config.get('web').get('visual').get('port') or 3001

SCALES_SERIALS = _config.get('scales') or []
OUTPUT_SERIALS = _config.get('output') or []

logging.basicConfig(level=LOGGER_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S",
                    filename="/var/log/scale-server/scales.log",
                    filemode='a')
