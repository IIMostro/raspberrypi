import time

import dht
import network
import uasyncio
import ujson
from machine import Pin
from umqtt.simple import MQTTClient

buzzer = Pin(16, Pin.OUT)
temperature_pin = Pin(5)
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


def read_temperature(pin: Pin):
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


async def publish_message(tempera, humidity, timestamp):
    msg = {
        "temperature": tempera,
        "humidity": humidity,
        "timestamp": timestamp
    }
    mqtt_client.publish("/esp8266/temperature".encode(), ujson.dumps(msg).encode())


async def buzzer_alter(pin: Pin, timing):
    pin.value(0)
    await uasyncio.sleep(timing)
    pin.value(1)


async def forever_read_temp():
    while True:
        temperature, humidity = read_temperature(temperature_pin)
        print(f'temperature: {temperature}, humidity:{humidity}')
        tasks = []
        if temperature > 33:
            tasks.append(uasyncio.gather(buzzer_alter(buzzer, 0.5)))
        tasks.append(uasyncio.gather(publish_message(temperature, humidity, time.time())))
        await uasyncio.gather(*tasks)
        await uasyncio.sleep(2)


async def main():
    await uasyncio.wait_for(connect_wifi("gonewiththewind", "wangtao0303"), 20)
    await uasyncio.wait_for(connect_mqtt("esp8266_temperature_client", "192.168.0.105"), 20)
    await uasyncio.gather(forever_read_temp())


if __name__ == '__main__':
    event_loop = uasyncio.get_event_loop()
    event_loop.create_task(main())
    event_loop.run_forever()

