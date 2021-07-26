from aiohttp import web
import asyncio
from asyncio import sleep as async_sleep
from os import path
from sys import path as sys_path
import aiohttp_jinja2
import jinja2


class Web:
    """
    Класс для работы с Web
    """

    def __init__(self, host: str, port: int, serial_list):
        self.serial_list = serial_list
        self.host = host
        self.port = port
        self.clients = []
        self.host_runners = []

        self.ROUTES = [
            web.get('/', self._send_simple),
            web.get(r'/{com:\d+}', self._send_simple),
        ]

        for serial in self.serial_list:
            serial.start()  # Открываем доступ к COM-PORT

    def _get_serial_data_by_id(self, id_serial: int) -> float:
        """
        Возвращает
        :param id_serial: Порядковый номер Com
        :return float: Полученный вес от Com
        """
        try:
            return self.serial_list[int(id_serial)].read()
        except [ValueError, IndexError]:
            return 0.0

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
            data = self._get_serial_data_by_id(request.match_info['com'])

            for websocket_client in self.clients:
                try:
                    await websocket_client.send_str(f"{data}")
                except ConnectionResetError:
                    self.clients.remove(websocket_client)
                await async_sleep(0.15)  # Задержка для снятия нагрузки с процессора

    @aiohttp_jinja2.template('websocket_weight.jinja2')
    async def _send_web_form(self, request: web.Request) -> dict:
        """
        # Отправка данных в браузер в простой форме
        :param request:
        :return:
        """

        try:
            data = self.serial_list[int(request.match_info['com'] if 'com' in request.match_info else 1)-1].read()
            return {'data': data}
        except [ValueError, IndexError]:
            return {'data': 'Ошибка'}

    async def _send_simple(self, request: web.Request) -> web.Response:
        """
        Отправка данных в простой форме
        """
        try:
            data = self.serial_list[int(request.match_info['com'] if 'com' in request.match_info else 1)-1].read()
            return web.Response(
                body=f"ves:{data/1000}"
            )
        except [ValueError, IndexError]:
            return web.Response(body='err')

    async def _start_site(self, app: web.Application, host: str, port: int) -> None:
        """
        Метод, создающий несколько серверов на одном сокете
        :param app: Приложение aiohttp web.Application
        :param host: Название хоста
        :param port : Номер порта
        :return:
        """

        runner = web.AppRunner(app)
        self.host_runners.append(runner)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        print(f"Запущен сервер {host}:{port}")

    def start(self) -> None:
        """
        Метод, запускающий передачу данных в web
        :return:
        """

        web_main = web.Application()
        web_sub = web.Application()  # Сервер для красивой формочки на экран, ибо кому-то лень поменять 1 строку в 1С

        web_main.add_routes(self.ROUTES)
        web_sub.add_routes([
            web.get('/', self._send_web_form),
            web.get(r'/{ws_weight:\d+}', self._weight_websocket),
        ])

        aiohttp_jinja2.setup(web_sub, loader=jinja2.FileSystemLoader(path.join(sys_path[0], 'templates')))

        loop = asyncio.get_event_loop()
        for serial in self.serial_list:
            loop.create_task(serial.background_reading())
        loop.create_task(self._start_site(web_main, host=self.host, port=self.port))
        loop.create_task(self._start_site(web_sub, host=self.host, port=self.port + 1))

        try:
            loop.run_forever()
        finally:
            for runner in self.host_runners:
                loop.run_until_complete(runner.cleanup())
