from aiohttp import web
import asyncio
from asyncio import sleep as async_sleep
from aiojobs.aiohttp import atomic
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
            data, message = self.serial.read()
            for websocket_client in self.clients:
                try:
                    if message != self.serial.EMPTY_DATA:
                        # Если com-port не пуст, отправляем данные веса
                        await websocket_client.send_str(f"{data}")
                    else:
                        # Если пуст, то отпавляем 0.0 и сообщение о том, что данные не поступают
                        await websocket_client.send_str(f"{data} / {message}")
                except ConnectionResetError:
                    self.clients.remove(websocket_client)
                await async_sleep(0.15)  # Задержка для снятия нагрузки с процессора

    async def _send_rest(self, _: web.Request) -> web.json_response():
        """
         # Отправка данных по REST API
        :param _:
        :return:
        """
        data, message = self.serial.read()

        if message != self.serial.EMPTY_DATA:
            # Если com-port не пуст, отправляем данные веса
            return web.json_response(status=200, data={'weight': data})
        else:
            # Если пуст, то отпавляем 0.0 и сообщение о том, что данные не поступают
            return web.json_response(status=200, data={'weight': data, 'message': message})

    @aiohttp_jinja2.template('websocket_weight.jinja2')
    async def _send_simple(self, _: web.Request) -> dict:
        """
        # Отправка данных в браузер в простой форме
        :param _:
        :return:
        """
        return {'host': f"{self.host}:{self.port}"}

    def start(self) -> None:
        """
        Метод, запускающий передачу данных в web
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self.serial.background_reading())
        web_app = web.Application()
        aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('templates'))
        web_app.add_routes(self.ROUTES)
        web.run_app(web_app, host=self.host, port=self.port)

