from machine import Pin, PWM
import time

p2 = PWM(Pin(14))
p2.freq(50)
p2.duty_u16(1638)
time.sleep(0.12)
p2.duty_u16(0)


def start(p2: PWM, s: float):
    p2.duty_u16(1638)
    time.sleep(s)
    p2.duty_u16(4915)