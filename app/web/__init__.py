from logging import getLogger, WARNING

from aiohttp import web
from asyncio import get_event_loop

from app.settings import config
from app.web import routes

_log = getLogger(__name__)
_host_runners: list = []
getLogger('aiohttp.access').setLevel(WARNING)

transmission = web.Application()
visual = web.Application(debug=False)

transmission.add_routes(routes=routes.transmission_routes)
visual.add_routes(routes=routes.visual_routes)


async def _start_site(app: web.Application, host: str, port: int):
    """
    Метод, создающий несколько серверов на одном сокете

    Args:
        app: Приложение aiohttp web.Application
        host: Адрес хоста
        port: Номер порта
    """
    runner = web.AppRunner(app)

    _host_runners.append(runner)

    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    _log.info(f"Запущен сервер {host}:{port}")


def start():
    loop = get_event_loop()
    loop.create_task(_start_site(transmission, host=config.TRANSMISSION_HOST, port=config.TRANSMISSION_PORT))
    loop.create_task(_start_site(visual, host=config.VISUAL_HOST, port=config.VISUAL_PORT))

    try:
        loop.run_forever()
    finally:
        for runner in _host_runners:
            loop.run_until_complete(runner.cleanup())
