from app.scales.scale_serial.base import SerialBase


class SerialOutput(SerialBase):
    """Класс для работы с COM-PORT на выводящие устройства"""

    def send_board(self, message: str):
        """
        Метод для отправки данных на табло

        Args:
            message: Данные для отображения на табло
        """
        self.serial.write(b'\x81\x20\x20' + str.encode(f"{int(message):05}") + b'\x20\x20\x0d\x0A')
