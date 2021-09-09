from app.fpylog import Log
from requests import get as requests_get
from asyncio import sleep as async_sleep
log = Log()


class WeightSocket:
    def __init__(self, host: str, output_serial=None):
        self.host = host
        self.output_serial = output_serial
        self.data = 0

        if self.output_serial is not None:
            for com in self.output_serial:
                if com.serial is None:
                    com.start()

    def read(self) -> int:
        request_data = requests_get(f"http://{self.host}/weight.html").text
        self.data = int(float(request_data if request_data else 0))

        # Если был передан ком-порт на вывод данных, то отправляем в него данные
        if self.output_serial is not None:
            for com in self.output_serial:
                try:
                    com.send_board(str(self.data))
                except AttributeError as err:
                    pass

        return self.data

    async def background_reading(self):
        while True:
            self.read()
            await async_sleep(0.2)

    def start(self):
        pass
