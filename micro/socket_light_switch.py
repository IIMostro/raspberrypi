import socket
import time

import network
import uasyncio
from machine import Pin, PWM
led = PWM(Pin(2, Pin.OUT))
led.freq(1000)


def connect_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print(f"esp8266 is already connection wifi, config:{wlan.ifconfig()}")
        return wlan
    wlan.active(True)
    print("connecting to wifi")
    wlan.connect(name, password)
    while not wlan.isconnected():
        print("connecting...")
        time.sleep(0.5)
    print(f"network config: {wlan.ifconfig()}\n")
    return wlan


def open_socket(ip='0.0.0.0', port=None) -> socket:
    udp_socket_connect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_connect.bind((ip, port))
    return udp_socket_connect


async def receive_message(connect: socket):
    while True:
        message, sender_info = connect.recvfrom(1024)
        message_str = message.decode("utf-8").strip()
        print("receive message:{} from {}".format(message_str, sender_info))
        if message_str == "on":
            await uasyncio.wait_for(open_led(), 20)
        if message_str == "off":
            await uasyncio.wait_for(off_led(), 20)


async def open_led():
    for i in range(1024, -1, -1):
        led.duty(i)
        time.sleep_us(500)


async def off_led():
    for i in range(0, 1024):
        led.duty(i)
        time.sleep_us(500)


if __name__ == '__main__':
    light = connect_wifi(name="gonewiththewind", password="wangtao0303")
    event_loop = uasyncio.get_event_loop()
    socket_connect = open_socket(port=8080)
    uasyncio.create_task(receive_message(socket_connect))
    event_loop.run_forever()
