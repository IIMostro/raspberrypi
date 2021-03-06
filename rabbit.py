"""
  @date 2020/8/24 11:29 下午
"""
__author__ = 'ilmostro'

import json
import sys
import time

import pika
from pika import PlainCredentials


class RabbitMqProperties(PlainCredentials):

    def __init__(self, username, password, host):
        super().__init__(username, password)
        self.host = host


class MessageQueue(object):

    def __init__(self, cred, exchange, routing_key, exchange_type="topic"):
        self.credentials = cred
        self.host = cred.host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=5672, credentials=cred))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key

    def producer(self, body):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=body)

    def consumer(self, callback, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(queue=queue_name, exchange=self.exchange, routing_key=self.routing_key)
        self.channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
        self.channel.start_consuming()


credentials = RabbitMqProperties(username='guest', password='guest', host="192.168.1.104")


def temperature(path):
    message_queue = MessageQueue(cred=credentials, exchange="raspberry.monitor", routing_key="temperature")
    while True:
        file = open(path)
        message = {"time": time.asctime(time.localtime(time.time())), "content": str(file.read())}
        message_queue.producer(json.dumps(message))
        time.sleep(1)
        file.close()


if __name__ == '__main__':
    argv = sys.argv
    temperature(str(sys.argv[1]))
