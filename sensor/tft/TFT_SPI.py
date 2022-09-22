import time

import machine


class SPI_BUS(object):
    def __init__(self):
        self.SCL = machine.Pin(13, machine.Pin.OUT)  # 初始值为0
        self.SDA = machine.Pin(14, machine.Pin.OUT)  # 初始值为0
        self.RES = machine.Pin(16, machine.Pin.OUT)  # 初始值为0
        self.DC = machine.Pin(17, machine.Pin.OUT)  # 初始值为0
        self.CS = machine.Pin(18, machine.Pin.OUT)  # 初始值为0
        self.BL = machine.Pin(19, machine.Pin.OUT)  # 初始值为0

    def SPI_WriteData(self, Data):
        for i in range(8):
            if Data & 0x80:
                self.SDA.value(1)
            else:
                self.SDA.value(0)
            self.SCL.value(0)
            self.SCL.value(1)
            Data <<= 1

    def Lcd_WriteIndex(self, Index):
        self.CS.value(0)
        self.DC.value(0)
        self.SPI_WriteData(Index)
        self.CS.value(1)

    def Lcd_WriteData(self, Data):
        self.CS.value(0)
        self.DC.value(1)
        self.SPI_WriteData(Data)
        self.CS.value(1)

    def LCD_WriteData_16Bit(self, Data):
        self.CS.value(0)
        self.DC.value(1)
        self.SPI_WriteData(Data >> 8)
        self.SPI_WriteData(Data)
        self.CS.value(1)

    def Lcd_WriteReg(self, Index, Data):
        self.Lcd_WriteIndex(Index)
        self.Lcd_WriteData(Data)

    def Lcd_Reset(self):
        self.RES.value(0)
        time.sleep(0.1)
        self.RES.value(1)
        time.sleep(0.05)
