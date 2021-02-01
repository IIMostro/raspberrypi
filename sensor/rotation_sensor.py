"""
  @date 2021/1/30 上午9:50
"""
__author__ = 'ilmostro'

import machine

adc = machine.ADC(0)
print(adc.read())
