import time

import dht
import network
import ntptime
import uasyncio
import ujson
import upip
from machine import Pin, Timer, SoftI2C
from umqtt.simple import MQTTClient

temperature_pin = Pin(14)
i2c = SoftI2C(scl=Pin(12), sda=Pin(13))

mqtt_client = None


async def connect_wifi(name, password):
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print(f"esp8266 is already connection wifi, config:{wlan.ifconfig()}")
        return wlan
    wlan.active(True)
    print("connecting to wifi")
    wlan.connect(name, password)
    while not wlan.isconnected():
        print("connecting...")
        await uasyncio.sleep(0.5)
    print(f"network config: {wlan.ifconfig()}\n")
    return wlan


async def read_temperature(pin: Pin):
    d = dht.DHT11(pin)
    d.measure()
    return d.temperature(), d.humidity()


def mqtt_callback(topic, msg):
    print(f"topic:{topic} receive message:{msg}")


async def connect_mqtt(client_id, host, port=1883, username=None, password=None, timeout=60):
    global mqtt_client
    mqtt_client = MQTTClient(client_id, host, port, username, password, timeout)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    print(f"mqtt client {client_id} already connected!")


async def pip_init_install():
    print("install umqtt....")
    upip.install("umqtt")
    print("install umqtt successed")


async def publish_tempera_message():
    tempera, humidity = await read_temperature(temperature_pin)
    msg = {
        "device": "root.home.living.temperature",
        "timestamp": (time.time() + 946656000) * 1000,
        "measurements": ["temperature", "humidity"],
        "values": [tempera, humidity]
    }
    print(msg)
    mqtt_client.publish("home.living".encode(), ujson.dumps(msg).encode())


async def publish_illuminance_message():
    intensity = await read_illuminance(i2c)
    msg = {
        "device": "root.home.living.illuminance",
        "timestamp": (time.time() + 946656000) * 1000,
        "measurements": ["intensity"],
        "values": [intensity]
    }
    print(msg)
    mqtt_client.publish("home.living".encode(), ujson.dumps(msg).encode())


async def read_illuminance(i2c: SoftI2C):
    i2c_addr = i2c.scan()
    if len(i2c_addr) != 1:
        return 0
    i2c.writeto(i2c_addr[0], b"\x01")
    i2c.writeto(i2c_addr[0], bytes([0x10]))
    await uasyncio.sleep(1)
    raw = i2c.readfrom(i2c_addr[0], 2)
    return ((raw[0] << 24) | (raw[1] << 16)) // 78642


async def forever_read_temp():
    while True:
        await uasyncio.gather(publish_tempera_message(), publish_illuminance_message())
        await uasyncio.sleep(2)


async def initialize_time():
    print("synchronization before time:" + str(time.localtime()))
    try:
        ntptime.NTP_DELTA = 3155644800
        ntptime.host = 'ntp1.aliyun.com'
        ntptime.settime()
        print("synchronization after time:" + str(time.localtime()))
    except OSError:
        await initialize_time()


def sync_initialize_time():
    await initialize_time()


async def main():
    await uasyncio.wait_for(connect_wifi("gonewiththewind", "wangtao0303"), 20)
    tasks = [
        pip_init_install(),
        initialize_time()
    ]
    await uasyncio.gather(*tasks)
    await uasyncio.wait_for(connect_mqtt("esp8266_temperature_client", "192.168.0.105", 1883, 'root', 'root'), 20)
    await uasyncio.gather(forever_read_temp())


if __name__ == '__main__':
    event_loop = uasyncio.get_event_loop()
    event_loop.create_task(main())
    sync_time_timer = Timer(1)
    sync_time_timer.init(period=1000 * 60 * 60 * 7, mode=Timer.PERIODIC, callback=sync_initialize_time)
    event_loop.run_forever()
