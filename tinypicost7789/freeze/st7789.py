import ustruct
import utime


class Display(object):
    _BUF = bytearray(4)

    width = 240
    height = 240

    def __init__(self, spi, dc, cs=None, rst=None):
        self.spi = spi
        self.dc = dc
        self.cs = cs or (lambda x: x)
        self.rst = rst or (lambda x: x)
        self.reset()

    def reset(self):
        self.rst(0)
        utime.sleep_ms(50)
        self.rst(1)
        utime.sleep_ms(50)
        self.cs(0)
        for command, data in (
            (b'\x36', b'\xc8'), # MADCTRL
            (b'\x3a', b'\x05'), # COLMOD
            (b'\xb2', # PORCTRL
             b'\x0c\x0c\x00\x33\x33'),
            (b'\xb7', b'\x35'), # GCTRL
            (b'\xbb', b'\x28'), # VCOMS
            (b'\xc0', b'\x2c'), # LCMCTRL
            (b'\xc2', b'\x01\xff'), # VDVVRHEN
            (b'\xc3', b'\x12'), # VRHS
            (b'\xc4', b'\x20'), # VDVSET
            (b'\xc6', b'\x0f'), # FRCTR2
            (b'\xd0', b'\xa4\xa1'),
            (b'\xe0', # PVGAMCTRL
             b'\xd0\x04\x0d\x11\x13\x28\x3f\x54\x4c\x18\x0d\x0b\x1f\x23'),
            (b'\xe1', # NVGAMCTRL
             b'\xd0\x04\x0C\x11\x13\x2c\x3f\x44\x51\x2f\x1f\x1f\x20\x23'),
            (b'\x2c', None),
            (b'\x21', None), # no invert
            (b'\x11', None), # display on
        ):
            self.write(command, data)
            utime.sleep_ms(10)
        utime.sleep_ms(120)
        self.write(b'\x29', None) # on
        self.cs(1)
        utime.sleep_ms(50)

    def write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.spi.write(command)
        if data:
            self.dc(1)
            self.spi.write(data)

    def block(self, x0, y0, x1, y1):
        y0 += 80
        y1 += 80
        ustruct.pack_into('>HH', self._BUF, 0, x0, x1)
        self.write(b'\x2a', self._BUF)
        ustruct.pack_into('>HH', self._BUF, 0, y0, y1)
        self.write(b'\x2b', self._BUF)
        self.write(b'\x2c')
        self.dc(1)

    def clear(self, color=0x00):
        self.cs(0)
        self.block(0, 0, self.width, self.height)
        chunks, rest = divmod(self.width * self.height, 512)
        pixel = ustruct.pack('>H', color)
        if chunks:
            data = pixel * 512
            for count in range(chunks):
                self.spi.write(data)
        if rest:
            self.spi.write(pixel * rest)
        self.cs(1)

    def __enter__(self):
        self.cs(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cs(1)
