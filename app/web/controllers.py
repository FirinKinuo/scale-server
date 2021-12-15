from logging import getLogger
from math import floor

from aiohttp import web

from app import SCALES
from app.web import pages
from app.settings import config
from app.scales import percent

log = getLogger(__name__)


async def send_weight_data(request: web.Request) -> web.Response:
    """Отправка данных в простой фо рме"""
    response = "error"
    try:
        scale_id = int(request.match_info.get('com') or 1) - 1
        scale = SCALES[scale_id]

        weight = scale.get_weight() * scale.weight_multiplier

        if weight is None:
            raise ValueError(f"{scale}: Данные с весов не могут быть получены!")

        response = f"ves:{scale.subtract_percent(weight) / 1000};vesreal:{weight / 1000}" if config.USE_PERCENT \
            else f"ves:{weight / 1000}"

        log.info(f"Запрошенный вес: {response}")
    except (ValueError, IndexError) as err:
        log.error(err)
    finally:
        return web.Response(body=response)


async def set_weight_percent(cls, request: web.Request) -> web.Response:
    """Установить процент деления веса"""
    weight_percent = request.query.get('value') or 0
    response = web.HTTPMovedPermanently(location="/getp")
    try:
        float(weight_percent)  # Проверяем, что передали число
        percent.set_weight_percent(weight=weight_percent)
        log.info(f"Установлен процент {weight_percent}")
    except ValueError:
        response = web.Response(body='Ошибка, значение должно быть числом')
    finally:
        return response


async def get_weight_percent(_: web.Request) -> web.Response:
    """Получить процент деления веса"""
    return web.Response(body=str(percent.get_weight_percent()))


async def send_web_form(request: web.Request) -> web.Response:
    """Отправка данных в браузер в простой форме"""
    response = pages.render_weight_visual_form(data="Ошибка")
    try:
        scale_id = int(request.match_info.get('com') or 1) - 1
        scale = SCALES[scale_id]

        weight = scale.get_weight()

        if weight is None:
            raise ValueError(f"{scale}: Данные с весов не могут быть получены!")

        response = pages.render_weight_visual_form(data=floor(weight))

    except (ValueError, IndexError) as err:
        log.error(err)

    finally:
        return web.Response(text=response, content_type="text/html")
