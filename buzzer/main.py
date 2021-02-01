"""
  @date 2021/1/31 下午10:16
"""
__author__ = 'ilmostro'

from machine import Pin, PWM
import music

buzzer = PWM(Pin(33, Pin.OUT), freq=440, duty=56)

music.play(music.NYAN, pin=Pin(33, Pin.OUT))