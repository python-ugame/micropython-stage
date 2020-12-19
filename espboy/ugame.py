"""
A helper module that initializes the display and buttons for the uGame
game console. See https://hackaday.io/project/27629-game
"""

from machine import SPI, I2C, Pin
import st7735r


K_LEFT = 0x01
K_UP = 0x02
K_DOWN = 0x04
K_RIGHT = 0x08
K_X = 0x10
K_O = 0x20
K_L = 0x40
K_R = 0x80


class Audio:
    def __init__(self):
        pass

    def play(self, audio_file):
        pass

    def stop(self):
        pass

    def mute(self, value=True):
        pass


class Buttons: # mcp23017
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        for register, value in (
            (0x00, b'\xff'), # port A input
            (0x01, b'\xff'), # port A polarity invert
            (0x06, b'\xff'), # port A pull-up
            (0x10, b'\xfe'), # port B input on all pins except B0
        ):
            self._i2c.writeto_mem(self._address, register, value)

    def _get_pressed(self):
        return self._i2c.readfrom_mem(self._address, 0x09, 1)

    def cs(self, value):
        # toggle the B0 pin for the display's CS
        self._i2c.writeto_mem(self._address, 0x19,
            b'\x01' if value else b'\x00')


i2c = I2C(sda=Pin(4), scl=Pin(5))
buttons = Buttons(i2c)
spi = SPI(1, baudrate=40000000)
display = st7735r.ST7735R(spi, Pin(16, Pin.OUT), buttons.cs)
audio = Audio()
