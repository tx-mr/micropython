# Goal - Display Neo-6M GPS data on the screen

from machine import Pin, UART
import time
import gc
import st7789 as ST7789
import rgb565 as color


class Display:
    def __init__(self):
        try:
            gc.enable()
            print("GC Enabled")

            print("Instantiate ST7789 class - Started")
            self.LCD = ST7789.ST7789()
            self.LCD.fill(color.BLACK)
            self.LCD.text("Waiting for GPS...", 2, 2, color.GREEN)
            self.LCD.show()
            print("Display Initialized")

        except Exception as e:
            print(f"An exception occurred: {e}")

    def update_display(self, latitude, lat_dir, longitude, lon_dir, speed):
        try:
            self.LCD.fill(color.BLACK)  # Clear the screen before updating
            self.LCD.text(f"Lat: {latitude} {lat_dir}", 2, 2, color.GREEN)
            self.LCD.text(f"Lon: {longitude} {lon_dir}", 2, 20, color.BLUE)
            self.LCD.text(f"Spd: {speed}", 2, 38, color.YELLOW)
            self.LCD.show()
            print("Display Updated with GPS Data, but still very tiny. Working on that!")

        except Exception as e:
            print(f"Problem updating display: {e}")

    def shutdown(self):
        try:
            self.LCD.fill(color.GREEN)
            self.LCD.show()
            print("Shut down, with a hint of green. Enjoy")

        except Exception as e:
            print(f"Problem shutting down: {e}")


def parse_gps(data):
    print(f"Processing GPS Data: {data}")
    data = data.decode('ascii').strip().split(',')

    # NMEA $GPRMC,hhmmss.ss,status,lat,lat_dir,long,long_dir,speed,course,date,mag_var,var_dir,mode,checksum

    if data[0] == '$GPRMC':
        time_utc = data[1]
        status = data[2]
        latitude = data[3]
        lat_dir = data[4]
        longitude = data[5]
        lon_dir = data[6]
        speed = data[7]
        date = data[9]

        if status == 'A':
            return latitude, lat_dir, longitude, lon_dir, speed
        else:
            print("Invalid GPS data")
            return None
    else:
        print("Non-GPRMC data received")
        return None


try:
    display = Display()
    print("Starting UART Connection")
    uart = UART(1, baudrate=9600, tx=Pin(43), rx=Pin(44), timeout=1000)
    time.sleep(2)
    print("Reading UART")
    while True:
        data = uart.readline()
        if data and (data.startswith(b'$GPRMC') or data.startswith(b'$GPGGA')):
            gps_data = parse_gps(data)
            if gps_data:
                latitude, lat_dir, longitude, lon_dir, speed = gps_data
                display.update_display(
                    latitude, lat_dir, longitude, lon_dir, speed)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Shutting down...")
    uart.deinit()
    display.shutdown()

except Exception as e:
    print(f"An error occurred: {e}")
    uart.deinit()
    display.shutdown()
