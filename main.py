import serial
import os
from os import environ
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def readSerial():
    while 1:
        try:
            opened_serial = serial.Serial(
                port=environ.get('COMPORT_PATH'),
                baudrate=environ.get('COMPORT_BAUDRATE'),
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=None
            )

            print(f"{opened_serial.port} открыт")

            # Проверка на наличие данных
            while not opened_serial.inWaiting():
                pass

            print(opened_serial.read())

        except serial.SerialException as err:
            print(err)


if __name__ == "__main__":
    readSerial()
