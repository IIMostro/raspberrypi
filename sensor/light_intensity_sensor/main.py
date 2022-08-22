"""
  @date 2021/1/31 下午4:28
"""
__author__ = 'ilmostro'

from machine import Pin
from machine import ADC
import time

sda = ADC(Pin(35))
scl = ADC(Pin(34))


def read_data():
    while True:
        print("sda:", round(sda.read()/(2 * 1.2)), " scl:", scl.read())
        time.sleep(1)


read_data()
