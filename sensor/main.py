"""
  @date 2021/1/30 下午4:18
"""
__author__ = 'ilmostro'

import time

import machine
from machine import PWM
from machine import Pin

adc = machine.ADC(0)

led_red_pin = Pin(5)
led_green_pin = Pin(4)
led_blue_pin = Pin(0)

led_red = PWM(led_red_pin, freq=1000)
led_green = PWM(led_green_pin, freq=1000)
led_blue = PWM(led_blue_pin, freq=1000)


def rgb_light(red, green, blue, brightness):
    pwm_red = led_red.duty(int(red / 255 * brightness * 1023))
    pwm_green = led_green.duty(int(green / 255 * brightness * 1023))
    pwm_blue = led_blue.duty(int(blue / 255 * brightness * 1023))


rgb_light(255, 255, 0, 1)

while True:
    brightness_temp = adc.read() / 1024
    print(brightness_temp)
    rgb_light(255, 255, 0, brightness_temp)
    time.sleep(0.01)
