# Library - Basic colors (RGB565)

def rgb565(red, green, blue):
    return ((red & 0xF8) << 8) | ((green & 0xFC) << 3) | (blue >> 3)


BLACK = rgb565(0, 0, 0)
WHITE = rgb565(255, 255, 255)
RED = rgb565(255, 0, 0)
GREEN = rgb565(0, 255, 0)
BLUE = rgb565(0, 0, 255)
CYAN = rgb565(0, 255, 255)
MAGENTA = rgb565(255, 0, 255)
YELLOW = rgb565(255, 255, 0)
ORANGE = rgb565(255, 165, 0)
PURPLE = rgb565(128, 0, 128)
GRAY = rgb565(128, 128, 128)
BROWN = rgb565(165, 42, 42)
