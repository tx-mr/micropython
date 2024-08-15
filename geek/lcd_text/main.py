# Board - ESP32-S3-Geek
# Goal - Display "Hello World"

from machine import Pin, PWM
import time
import gc
import st7789 as ST7789
import rgb565 as color
import math

class Display:
    def __init__(self):
        try:
            gc.enable()
            print("GC Enabled")

            print("Instantiate ST7789 class - Started")
            self.LCD = ST7789.ST7789()

            print("set window")
            self.LCD.set_window()

            print("Hello, world!")
            self.LCD.fill(color.BLACK)
            self.LCD.text("Hello, World!", 10, 10, color.WHITE)
            self.LCD.show()
            
            time.sleep(5)
            
            print("Texas style! (kinda)")
            self.LCD.fill(color.BLACK)
            self.draw_texas_flag()
            self.LCD.text("Hello, World!", 90, 20, color.YELLOW)
            self.LCD.show()
            
            print("Display Complete")
        except Exception as e:
            print(f"An exception occurred: {e}")

    def shutdown(self):
        try:
            self.LCD.fill(color.ORANGE)
            self.LCD.show()
            print("Display filled with orange just for fun")
        except Exception as e:
            print(f"Problem shutting down: {e}")

    def draw_star(self, center_x, center_y, radius, color):
        points = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            points.append((x, y))

        for i in range(5):
            self.LCD.line(points[i][0], points[i][1], points[(i + 2) % 5][0], points[(i + 2) % 5][1], color)

    def draw_texas_flag(self):
        self.LCD.fill_rect(0, 0, 79, 135, color.BLUE)
        self.LCD.fill_rect(80, 0, 240, 64, color.RED)
        self.LCD.fill_rect(80, 65, 240, 135, color.WHITE)

        star_center_x = 40
        star_center_y = 67
        star_radius = 30

        self.draw_star(star_center_x, star_center_y, star_radius, color.WHITE)

try:
    display = Display()
    while True:
        time.sleep_ms(100)
except KeyboardInterrupt:
    display.shutdown()
