from random import random

import paho.mqtt.client as mqtt

client = mqtt.Client()
connection = client.connect(host='192.168.120.20', port=1883, keepalive=600)
queue = "simple_mqtt_queue"
client_id = f'python-mqtt-{random.randint(0, 100)}'


def subscribe():
    def on_message(self, user_data, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(queue)
    client.on_message = on_message
    client.loop_forever()


if __name__ == '__main__':
    subscribe()
