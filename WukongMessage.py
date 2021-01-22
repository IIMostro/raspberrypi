"""
  @date 2020/8/24 11:29 下午
"""
__author__ = 'ilmostro'

from datetime import datetime

import pika
from elasticsearch import Elasticsearch
from pika import PlainCredentials

es = Elasticsearch("192.168.1.107:9200")


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

    def consumer(self, callback, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(queue=queue_name, exchange=self.exchange, routing_key=self.routing_key)
        self.channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
        self.channel.start_consuming()


def message(w, x, y, body):
    data = {
        "@timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
        "message": body
    }
    es.index(index="wukong-logs", doc_type="book", body=data)


credentials = RabbitMqProperties(username='guest', password='guest', host="192.168.1.104")

if __name__ == '__main__':
    message_queue = MessageQueue(cred=credentials, exchange="logs-exchange", routing_key="#")
    message_queue.consumer(lambda w, x, y, z: message, "wukong-queue")
