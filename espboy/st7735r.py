import ustruct
import utime


class ST7735R:
    width = 128
    height = 128

    def __init__(self, spi, dc, cs, rotation=0x06):
        self.spi = spi
        self.dc = dc
        self.dc(1)
        self.cs = cs
        self.cs(0)
        self.rotation = rotation
        utime.sleep_ms(100)
        for command, data, delay in (
            (b'\x01', b'', 120),
            (b'\x11', b'', 120),
            (b'\x36', bytes(((rotation & 0x07) << 5,)), 0),
            (b'\x3a', b'\x05', 0),
            (b'\xb4', b'\x07', 0),
            (b'\xb1', b'\x01\x2c\x2d', 0),
            (b'\xb2', b'\x01\x2c\x2d', 0),
            (b'\xb3', b'\x01\x2c\x2d\x01\x2c\x2d', 0),
            (b'\xc0', b'\x02\x02\x84', 0),
            (b'\xc1', b'\xc5', 0),
            (b'\xc2', b'\x0a\x00', 0),
            (b'\xc3', b'\x8a\x2a', 0),
            (b'\xc4', b'\x8a\xee', 0),
            (b'\xc5', b'\x0e', 0),
            (b'\x20', b'', 0),
            (b'\xe0', b'\x02\x1c\x07\x12\x37\x32\x29\x2d'
             b'\x29\x25\x2B\x39\x00\x01\x03\x10', 0),
            (b'\xe1', b'\x03\x1d\x07\x06\x2E\x2C\x29\x2D'
             b'\x2E\x2E\x37\x3F\x00\x00\x02\x10', 0),
            (b'\x13', b'', 10),
            (b'\x29', b'', 120),
        ):
            self.write(command, data)
            utime.sleep_ms(delay)
        self.dc(0)
        self.cs(1)

    def block(self, x0, y0, x1, y1):
        if self.rotation & 0x01:
            x0 += 3 # 32 # alternate st7735 display
            x1 += 3 # 32
            y0 += 2 # 0
            y1 += 2 # 0
        else:
            x0 += 2 # 0
            x1 += 2 # 0
            y0 += 3 # 32
            y1 += 3 # 32
        xpos = ustruct.pack('>HH', x0, x1)
        ypos = ustruct.pack('>HH', y0, y1)
        self.write(b'\x2a', xpos)
        self.write(b'\x2b', ypos)
        self.write(b'\x2c')
        self.dc(1)

    def write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.spi.write(command)
        if data:
            self.dc(1)
            self.spi.write(data)

    def clear(self, color=0x00):
        self.block(0, 0, self.width - 1, self.height - 1)
        pixel = color.to_bytes(2, 'big')
        data = pixel * 256
        for count in range(self.width * self.height // 256):
            self.write(None, data)

    def __enter__(self):
        self.cs(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cs(1)
