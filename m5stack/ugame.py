"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

from machine import SPI, I2C, Pin
import ili9341


K_X = 0x20
K_DOWN = 0x01
K_LEFT = 0x08
K_RIGHT = 0x04
K_UP = 0x02
K_O = 0x10


class Audio:
    def __init__(self):
        pass

    def play(self, audio_file):
        pass

    def stop(self):
        pass

    def mute(self, value=True):
        pass


class Buttons:
    def __init__(self, i2c, address=0x10):
        self._i2c = i2c
        self._address = address

    def get_pressed(self):
        return self._i2c.readfrom(self._address, 1)[0]


spi = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23))
display = ili9341.Display(spi, Pin(27, Pin.OUT), Pin(14, Pin.OUT),
                          Pin(33, Pin.OUT))
lite = Pin(32, Pin.OUT)
lite(1)
i2c = I2C(sda=Pin(21), scl=Pin(22))
buttons = Buttons(i2c)
audio = Audio()
