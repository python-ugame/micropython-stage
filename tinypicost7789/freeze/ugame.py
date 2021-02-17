"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

from machine import SPI, I2C, Pin
import st7789
import struct


K_DOWN = 0x0800
K_LEFT = 0x1000
K_RIGHT = 0x2000
K_UP = 0x8000
K_O = 0x0001
K_X = 0x0002
K_Z = 0x0008


class Audio:
    def __init__(self):
        pass

    def play(self, audio_file):
        pass

    def stop(self):
        pass

    def mute(self, value=True):
        pass


class Buttons: # mpr121
    def __init__(self, i2c, address=0x5a):
        self._i2c = i2c
        self._address = address
        for register, value in (
            (0x80, b'\x63'), # reset
            (0x5e, b'\x00'), # stop mode, reset config
            (0x2b, b'\x01\x01\x10\x20\x01\x01\x10\x20\x01\x10\xff'),
            (0x5b, b'\x00\x10\x20'), # debounce, config1, config2
            (0x5e, b'\x8f'), # exit stop mode
        ):
            self._i2c.writeto_mem(self._address, register, value)

    def get_pressed(self):
        buffer = self._i2c.readfrom_mem(self._address, 0x00, 2)
        mask = struct.unpack('>H', buffer)[0]
        return mask


spi = SPI(2, baudrate=40_000_000, sck=Pin(18), mosi=Pin(23))
display = st7789.Display(spi, Pin(4, Pin.OUT), Pin(14, Pin.OUT))
display.clear()
i2c = I2C(sda=Pin(21), scl=Pin(22))
buttons = Buttons(i2c)
audio = Audio()
