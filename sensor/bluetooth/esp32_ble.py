from time import sleep_ms

import bluetooth
from machine import Pin

BLE_MSG = ""


class ESP32_BLE():
    def __init__(self, name):
        self.led = Pin(14, Pin.OUT)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def ble_irq(self, event, data):
        global BLE_MSG
        if event == 1:  # _IRQ_CENTRAL_CONNECT 手机链接了此设备
            self.led.value(0)
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT 手机断开此设备
            self.advertiser()
            self.led.value(1)
        elif event == 3:  # _IRQ_GATTS_WRITE 手机发送了数据
            buffer = self.ble.gatts_read(self.rx)
            BLE_MSG = buffer.decode('UTF-8').strip()


    def register(self):
        service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        # 这个services代表的是一个服务，例如一个蓝牙可以做很多事情，温度接收，光照接收，这就是两个服务
        services = (
            (
                # 初始化一个服务的uuid
                bluetooth.UUID(service_uuid),
                (
                    # 服务发送的uuid
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    # 服务接收的uuid
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ),
        )
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(services)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("\r\n")


if __name__ == "__main__":
    ble = ESP32_BLE("ESP32BLE")

    while True:
        if BLE_MSG == 'read_LED':
            print(BLE_MSG)
            ble.send('hello' + BLE_MSG)
            BLE_MSG = ""
        sleep_ms(100)