"""Это самая странная и костыльная часть проекта, ибо 1Сники - пидоры"""
from typing import Any


def render_weight_visual_form(data: Any) -> str:
    """
    Рендер визуальной формы данных веса
    Args:
        data (typing.Any): Данные веса, которые необходимо вывести

    Returns:
        str - Рендер страницы
    """
    return f"""<!DOCTYPE HTML PUBLIC />
<html>
<head>
    <meta http-equiv=Refresh content=1>
    <title>auto</title>
    <style> html, body {{
        background-color: green;
        background: linear-gradient(to top, #648520, #8aa652);
        overflow: hidden;
    }}

    div {{
        color: white;
        text-align: center;
        font-size: 30px;
        font-family: sans-serif;
    }} </style>
</head>
<body>
<div id=subscribe>{data}</div>
</body>
</html>"""
