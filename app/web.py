from aiohttp import web, WSMsgType


class Web:
    def __init__(self, host: str, port: int, serial):
        self.serial = serial
        self.host = host
        self.port = port

        self.serial.start()  # Открываем доступ к COM-PORT

    async def _send_data(self, request):
        def use_api(response_status, response_json):
            return web.json_response(status=response_status, data=response_json)

        # TODO: Make Сделать отправку по websocket
        async def use_websocket(ws_request, response_data):
            return web.Response(body=f"{response_data}")

        data, message = self.serial.read()

        if message != self.serial.EMPTY_DATA:
            if request.path_qs == '/api':
                return use_api(response_status=200, response_json={'weight': data})
            else:
                return use_websocket(request, response_data=data)
        else:
            return web.json_response(status=200, data={
                'message': message
            })

    def start(self):
        web_app = web.Application()

        web_app.add_routes([
            web.get('/', self._send_data),
            web.get('/api', self._send_data)
        ])

        web.run_app(web_app, host=self.host, port=self.port)
