import time

from machine import Pin

Trig, Echo = Pin(4, Pin.OUT), Pin(5, Pin.IN)
Trig.value(0)
Echo.value(0)


def distance(trig: Pin, echo: Pin):

    # 给一个高电平，发送8个40KHZ的声波
    trig.value(1)
    time.sleep_us(10)
    # 复位
    trig.value(0)
    # 给回声复位
    while echo.value() == 0:
        pass
    # 开始计时
    t1 = time.ticks_us()
    # 等待回声返回
    while echo.value() == 1:
        pass
    # 回声返回时间
    t2 = time.ticks_us()
    t3 = time.ticks_diff(t2, t1) / 8000
    # 计算距离
    return t3 * 340 / 2
