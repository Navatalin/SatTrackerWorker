import json
import pika
from pika.exchange_type import ExchangeType

class MqPublish:
    def __init__(self) -> None:
        self._connection = None
        self._channel = None

    def connect(self):
        print('connecting to mq')
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=pika.PlainCredentials('Worker','workerPassword')))
        print('connected, getting channel')
        self._channel = self._connection.channel()
        print('got channel, delcaring exchange')
        self._channel.exchange_declare('SatWorker',exchange_type=ExchangeType.topic,durable=True)

    def publish_message(self, message):
        self._channel.basic_publish(exchange='SatWorker',routing_key='Out',body=json.dumps(message))

    def disconnect(self):
        self._connection.close()