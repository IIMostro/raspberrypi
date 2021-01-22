"""
  @date 2020/8/27 10:48 下午
"""
__author__ = 'ilmostro'

from rabbit import MessageQueue, credentials


def consumer(temperature):
    print(str(temperature, encoding="utf-8"))


if __name__ == '__main__':
    message_queue = MessageQueue(cred=credentials, exchange="raspberry.monitor", routing_key="temperature")
    message_queue.consumer(lambda w, x, y, z: consumer(z), "raspberry.temperature")
