from ast import literal_eval
from app.settings import config


def get_weight_percent() -> float:
    try:
        with open(config.PERCENT_SAVE_PATH, 'r', encoding='utf-8') as percent_file:
            weight_percent = str(literal_eval(percent_file.read()).get('weight_percent')).replace(',', '.')
    except FileNotFoundError:
        weight_percent = 0

    return float(weight_percent)


def set_weight_percent(weight: float):
    with open(config.PERCENT_SAVE_PATH, 'w', encoding='UTF-8') as percent_file:
        percent_file.write(str({'weight_percent': weight}))  # Сохраняем в файл значение процента
