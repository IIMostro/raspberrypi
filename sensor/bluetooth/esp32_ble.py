from time import sleep_ms

import bluetooth
from machine import Pin, Timer
import network

BLE_MSG = ""


class ESP32_BLE:

    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.led.off()
        self.timer.deinit()

    def disconnected(self):
        self.timer.init(mode=Timer.PERIODIC, period=100, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global BLE_MSG
        ## 时间手机链接了此设备
        if event == 1:
            self.connected()
            ## 断开链接
        elif event == 2:
            self.advertiser()
            self.disconnected()
        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            BLE_MSG = buffer.decode("UTF-8").strip()
        pass

    def register(self):
        service_uuid = "1a4361f1-0bbe-4c1c-a94a-7fdb2d7b4675"
        reader_uuid = "1a4361f1-0bbe-4c1c-a94a-7fdb2d7b4675"
        sender_uuid = "1a4361f1-0bbe-4c1c-a94a-7fdb2d7b4675"

        services = (
            (
                bluetooth.UUID(service_uuid),
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ),
        )
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(services)

    def send(self, message):
        self.ble.gatts_notify(0, self.tx, message + "\n")

    def advertiser(self):
        name = bytes(self.name, "UTF-8")
        adv_data = bytearray("\x02\x02\x02") + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


def buttons_irq(pin):
    pass

def connect_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        # print(f"esp8266 is already connection wifi, config:{wlan.ifconfig()}")
        return wlan
    wlan.active(True)
    print("connecting to wifi")
    wlan.connect(name, password)
    while not wlan.isconnected():
        print("connecting...")
        sleep_ms(100)
    return wlan


if __name__ == '__main__':
    connect_wifi("gonewiththewind", "wangtao0303")
    ble = ESP32_BLE("esp32-bluetooth")
    but = Pin(0, Pin.IN)
    but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)
    led = Pin(2, Pin.OUT)
    while True:
        if BLE_MSG == "read":
            print(BLE_MSG)
            BLE_MSG = ""
            print("led is on")
            ble.send("led is on")
        sleep_ms(100)
