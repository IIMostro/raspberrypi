from machine import Pin, PWM
import time

'''
    呼吸灯演示
'''
led2 = PWM(Pin(2, Pin.OUT))
led2.freq(1000)
while True:
    for i in range(0, 1024):
        led2.duty(i)
        time.sleep_ms(2)
    for i in range(1024, -1, -1):
        led2.duty(i)
        time.sleep_ms(2)