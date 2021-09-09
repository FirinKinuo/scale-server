from re import match as re_match


def is_ip_string(string_to_check: str) -> bool:
    """
    Проверяет, является ли строка IP адрессом
    :param string_to_check: str Строка для проверки
    :return bool: True - если строка является IP. False - если не является
    """

    regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    return re_match(regex, string_to_check) is not None
