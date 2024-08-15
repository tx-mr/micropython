# Library - ST7789 IPS LCD Driver
# Resource URL - https://www.waveshare.com/w/upload/a/ae/ST7789_Datasheet.pdf
# Extra inspiration taken from LCD Demo code - https://files.waveshare.com/wiki/ESP32-S3-GEEK/ESP32-S3-GEEK_Code.zip

from machine import Pin, SPI, PWM
import framebuf
import time

# Pins
PIN_BL = 7
PIN_DC = 8
PIN_RST = 9
PIN_CS = 10
PIN_MOSI = 11
PIN_SCK = 12

# SPI Clock speed
SPI_CLOCK_HZ = 50000000

# ST7789 Full Command Library
ST7789_NOP = 0x00 #No op
ST7789_SWRESET = 0x01 #Software Reset
ST7789_RDDID = 0x04 #Read Display ID
ST7789_RDDST = 0x09 #Read Display Status
ST7789_RDDPM = 0x0A #Read Display Power Mode
ST7789_RDDMADCTL = 0x0B #Read Display MADCTL
ST7789_RDDCOLMOD = 0x0C #Read Display Pixel Format
ST7789_RDDIM = 0x0D #Read Display Image Mode
ST7789_RDDSM = 0x0E #Read Display Signal Mode
ST7789_RDDSDR = 0x0F #Read Display Self-Diagnostic Result
ST7789_SLPIN = 0x10 #Sleep in
ST7789_SLPOUT = 0x11 #Sleep Out
ST7789_PTLON = 0x12 #Partial Display Mode On
ST7789_NORON = 0x13 #Normal Display Mode On
ST7789_INVOFF = 0x20 #Display Inversion Off
ST7789_INVON = 0x21 #Display Inversion On
ST7789_GAMSET = 0x26 #Gamma Set
ST7789_DISPOFF = 0x28 #Display Off
ST7789_DISPON = 0x29 #Display On
ST7789_CASET = 0x2A #Column Address Set
ST7789_RASET = 0x2B #Row Address Set
ST7789_RAMWR = 0x2C #Memory Write
ST7789_RAMRD = 0x2E #Memory Read
ST7789_PTLAR = 0x30 #Partial Area
ST7789_VSCRDEF = 0x33 #Vertical Scrolling Definition
ST7789_TEOFF = 0x34 #Tearing Effect Line OFF
ST7789_TEON = 0x35 #Tearing Effect Line On
ST7789_MADCTL = 0x36 #Memory Data Access Control
ST7789_VSCSAD = 0x37 #Vertical Scroll Start Address of RAM
ST7789_IDMOFF = 0x38 #Idle Mode Off
ST7789_IDMON = 0x39 #Idle mode on
ST7789_COLMOD = 0x3A #Interface Pixel Format
ST7789_WRMEMC = 0x3C #Write Memory Continue
ST7789_RDMEMC = 0x3E #Read Memory Continue
ST7789_STE = 0x44 #Set Tear Scanline
ST7789_GSCAN = 0x45 #Get Scanline
ST7789_WRDISBV = 0x51 #Write Display Brightness
ST7789_RDDISBV = 0x52 #Read Display Brightness Value
ST7789_WRCTRLD = 0x53 #Write CTRL Display
ST7789_RDCTRLD = 0x54 #Read CTRL Value Display
ST7789_WRCACE = 0x55 #Write Content Adaptive Brightness Control and Color Enhancement
ST7789_RDCABC = 0x56 #Read Content Adaptive Brightness Control
ST7789_WRCABCMB = 0x5E #Write CABC Minimum Brightness
ST7789_RDCABCMB = 0x5F #Read CABC Minimum Brightness
ST7789_RDABCSDR = 0x68 #Read Automatic Brightness Control Self-Diagnostic Result
ST7789_RAMCTRL = 0xB0 #RAM Control
ST7789_RGBCTRL = 0xB1 #RGB Interface Control
ST7789_PORCTRL = 0xB2 #Porch Setting
ST7789_FRCTRL1 = 0xB3 #Frame Rate Control 1 (In partial mode/ idle colors)
ST7789_PARCTRL = 0xB5 #Partial Control
ST7789_GCTRL = 0xB7 #Gate Control
ST7789_GTADJ = 0xB8 #Gate On Timing Adjustment
ST7789_DGMEN = 0xBA #Digital Gamma Enable
ST7789_VCOMS = 0xBB #VCOM Setting
ST7789_POWSAV = 0xBC #Power Saving Mode
ST7789_DLPOFFSAVE = 0xBD #Display off power save
ST7789_LCMCTRL = 0xC0 #LCM Control
ST7789_IDSET = 0xC1 #ID Code Setting
ST7789_VDVVRHEN = 0xC2 #VDV and VRH Command Enable
ST7789_VRHS = 0xC3 #VRH Set
ST7789_VDVS = 0xC4 #VDV Set
ST7789_VCMOFSET = 0xC5 #VCOM Offset Set
ST7789_FRCTRL2 = 0xC6 #Frame Rate Control in Normal Mode
ST7789_CABCCTRL = 0xC7 #CABC Control
ST7789_REGSEL1 = 0xC8 #Register Value Selection 1
ST7789_REGSEL2 = 0xCA #Register Value Selection 2
ST7789_PWMFRSEL = 0xCC #PWM Frequency Selection
ST7789_PWCTRL1 = 0xD0 #Power Control 1
ST7789_VAPVANEN = 0xD2 #Enable VAP/VAN signal output
ST7789_RDID1 = 0xDA #Read ID1
ST7789_RDID2 = 0xDB #Read ID2
ST7789_RDID3 = 0xDC #Read ID3
ST7789_CMD2EN = 0xDF #Command 2 Enable
ST7789_PVGAMCTRL = 0xE0 #Positive Voltage Gamma Control
ST7789_NVGAMCTRL = 0xE1 #Negative Voltage Gamma Control
ST7789_DGMLUTR = 0xE2 #Digital Gamma Look-up Table for Red
ST7789_DGMLUTB = 0xE3 #Digital Gamma Look-up Table for Blue
ST7789_GATECTRL = 0xE4 #Gate Control
ST7789_SPI2EN = 0xE7 #SPI2 Enable
ST7789_PWCTRL2 = 0xE8 #Power Control 2
ST7789_EQCTRL = 0xE9 #Equalize time control
ST7789_PROMCTRL = 0xEC #Program Mode Control
ST7789_PROMEN = 0xFA #Program Mode Enable
ST7789_NVMSET = 0xFC #NVM Setting
ST7789_PROMACT = 0xFE #Program action

class ST7789(object, framebuf.FrameBuffer):
    def __init__(
        self,
        port=1,
        cs=PIN_CS,
        dc=PIN_DC,
        rst=PIN_RST,
        bl=PIN_BL,
        spi_speed_hz=SPI_CLOCK_HZ,
        width=240,
        height=135,
        rotation=0,
        offset_left=0,
        offset_top=0,
        invert=False,
    ):
        print("Initializing ST7789 class")
        self.width = width
        self.height = height
        self.rotation = rotation
        self.offset_left = offset_left
        self.offset_top = offset_top
        self.invert = invert

        self.cs = Pin(cs, Pin.OUT)
        self.dc = Pin(dc, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(port, baudrate=spi_speed_hz, polarity=0, phase=0, sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=None)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        
        self.backlight = PWM(Pin(bl))
        self.backlight.freq(1000)
        self.backlight.duty_u16(65535)
        
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

        self.init_display()
        
    def init_display(self):
        # Manual reset to clear previous
        self.rst(1)
        self.rst(0)
        self.rst(1)        
        
        print("Initializing display")
        self.write_cmd(ST7789_SWRESET)
        time.sleep(0.150)

        self.write_cmd(ST7789_MADCTL)
        self.write_data(0x70)

        self.write_cmd(ST7789_PORCTRL)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(ST7789_COLMOD)
        self.write_data(0x05)

        self.write_cmd(ST7789_GCTRL)
        self.write_data(0x14)

        self.write_cmd(ST7789_VCOMS)
        self.write_data(0x37)

        self.write_cmd(ST7789_LCMCTRL)
        self.write_data(0x2C)

        self.write_cmd(ST7789_VDVVRHEN)
        self.write_data(0x01)

        self.write_cmd(ST7789_VRHS)
        self.write_data(0x12)

        self.write_cmd(ST7789_VDVS)
        self.write_data(0x20)

        self.write_cmd(ST7789_PWCTRL1)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(ST7789_FRCTRL2)
        self.write_data(0x0F)

        self.write_cmd(ST7789_PVGAMCTRL)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(ST7789_NVGAMCTRL)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        if self.invert:
            self.write_cmd(ST7789_INVOFF)
        else:
            self.write_cmd(ST7789_INVON)

        self.write_cmd(ST7789_SLPOUT)

        self.write_cmd(ST7789_DISPON)
        time.sleep(0.100)
        
        print("Display initialized")

    def show(self):
        self.write_cmd(ST7789_CASET)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(ST7789_RASET)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(ST7789_RAMWR)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.swap()
        self.spi.write(self.buffer)
        self.swap()
        self.cs(1)

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        if x1 is None:
            x1 = self.width - 1

        if y1 is None:
            y1 = self.height - 1

        y0 += self.offset_top
        y1 += self.offset_top

        x0 += self.offset_left
        x1 += self.offset_left

        self.write_cmd(ST7789_CASET)
        self.write_data(x0 >> 8)
        self.write_data(x0 & 0xFF)
        self.write_data(x1 >> 8)
        self.write_data(x1 & 0xFF)
        self.write_cmd(ST7789_RASET)
        self.write_data(y0 >> 8)
        self.write_data(y0 & 0xFF)
        self.write_data(y1 >> 8)
        self.write_data(y1 & 0xFF)
        self.write_cmd(ST7789_RAMWR)

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    @micropython.viper
    def swap(self):
        buf=ptr8(self.buffer)
        for x in range(0,240*135*2,2):
            tt=buf[x]
            buf[x]=buf[x+1]
            buf[x+1]=tt
            
    @micropython.viper
    def ins(self,ins_data,ins_len:int,start:int):
        ins_buf=ptr8(ins_data)
        buf=ptr8(self.buffer)
        for x in range(ins_len):
            buf[start+x]=ins_buf[x]
            
    @micropython.viper
    def mirror(self):
        buf=ptr8(self.buffer)
        for y in range(0,135):
            for x in range(0,120):
                temp_x=(240-x)*2
                temp_y=y*480
                t1=buf[x*2+temp_y]
                t2=buf[x*2+temp_y+1]
                buf[x*2+temp_y]=buf[temp_x+temp_y]
                buf[x*2+temp_y+1]=buf[temp_x+temp_y+1]
                buf[temp_x+temp_y]=t1
                buf[temp_x+temp_y+1]=t2
