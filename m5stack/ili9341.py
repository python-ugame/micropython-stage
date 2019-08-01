import ustruct
import utime


class Display(object):
    _BUF = bytearray(4)

    width = 320
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
            (b'\xef', b'\x03\x80\x02'),
            (b'\xcf', b'\x00\xc1\x30'),
            (b'\xed', b'\x64\x03\x12\x81'),
            (b'\xe8', b'\x85\x00\x78'),
            (b'\xcb', b'\x39\x2c\x00\x34\x02'),
            (b'\xf7', b'\x20'),
            (b'\xea', b'\x00\x00'),
            (b'\xc0', b'\x23'),  # Power Control 1, VRH[5:0]
            (b'\xc1', b'\x10'),  # Power Control 2, SAP[2:0], BT[3:0]
            (b'\xc5', b'\x3e\x28'),  # VCM Control 1
            (b'\xc7', b'\x86'),  # VCM Control 2
            (b'\x36', b'\x10'),  # Memory Access Control
            (b'\x3a', b'\x55'),  # Pixel Format
            (b'\xb1', b'\x00\x18'),  # FRMCTR1
            (b'\xb6', b'\x08\x82\x27'),  # Display Function Control
            (b'\xf2', b'\x00'),  # 3Gamma Function Disable
            (b'\x26', b'\x01'),  # Gamma Curve Selected
            (b'\xe0',  # Set Gamma
             b'\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00'),
            (b'\xe1',  # Set Gamma
             b'\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f'),
            (b'\x11', None),
            (b'\x29', None),
        ):
            self.write(command, data)
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
