"""
  @date 2021/1/31 下午7:38
"""
__author__ = 'ilmostro'

from machine import Pin
from machine import ADC
import time

temp = ADC(Pin(35))

while True:
    print("temperature", temp.read())
    time.sleep(1)