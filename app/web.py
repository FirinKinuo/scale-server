from aiohttp import web
import asyncio
from asyncio import sleep as async_sleep
import aiohttp_jinja2
import jinja2


class Web:
    """
    Класс для работы с Web
    """

    def __init__(self, host: str, port: int, serial):
        self.serial = serial
        self.host = host
        self.port = port
        self.clients = []

        self.ROUTES = [
            web.get('/', self._send_simple),
            web.get('/web', self._send_web_form),
            web.get('/ws_weight', self._weight_websocket),
            web.get('/api', self._send_rest)
        ]

        self.serial.start()  # Открываем доступ к COM-PORT

    async def _weight_websocket(self, request: web.Request) -> None:
        """
        Метод для отправки данных по websocket
        :param request:
        :return:
        """
        websocket = web.WebSocketResponse()
        await websocket.prepare(request)
        self.clients.append(websocket)

        # Цикл, который читает com-port и отправляет данные в websocket
        while True:
            data = self.serial.read()

            for websocket_client in self.clients:
                try:
                    await websocket_client.send_str(f"{data}")
                except ConnectionResetError:
                    self.clients.remove(websocket_client)
                await async_sleep(0.15)  # Задержка для снятия нагрузки с процессора

    async def _send_rest(self, _: web.Request) -> web.json_response():
        """
         # Отправка данных по REST API
        :param _:
        :return:
        """
        data = self.serial.read()
        return web.json_response(status=200, data={'weight': data})

    @aiohttp_jinja2.template('websocket_weight.jinja2')
    async def _send_simple(self, _: web.Request) -> dict:
        """
        # Отправка данных в браузер в простой форме
        :param _:
        :return:
        """
        return

    @aiohttp_jinja2.template('websocket_weight.jinja2')
    async def _send_web_form(self, _: web.Request) -> dict:
        """
        # Отправка данных в браузер в простой форме
        :param _:
        :return:
        """
        return {'web_form': True}

    def start(self) -> None:
        """
        Метод, запускающий передачу данных в web
        :return:
        """

        web_app = web.Application()
        aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('templates'))

        loop = asyncio.get_event_loop()
        loop.create_task(self.serial.background_reading())
        web_app.add_routes(self.ROUTES)

        print("\033[35mДоступные URI:\n\033[37m"
              "\033[35m/\033[37m    - Простой вывод данных\n"
              "\033[35m/web\033[37m - вывод веб-формы\n"
              "\033[35m/api\033[37m - получение данных по REST")

        web.run_app(web_app, host=self.host, port=self.port)

