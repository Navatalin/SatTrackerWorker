from numpy import true_divide
import pika
from pika.exchange_type import ExchangeType
import json
from Tracking import Tracking
from mqpublish import MqPublish

mq = MqPublish()
tracking = Tracking()

def process_message(ch, method, properties, body):
    sat_names = json.loads(body)
    tracking.get_pos(sat_names, mq)

def main():
    mq.connect()

    print('connecting to mq')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=pika.PlainCredentials('Worker','workerPassword')))
    print('connected, getting channel')
    channel = connection.channel()
    print('got channel, delcaring exchange')
    channel.exchange_declare('SatWorker',exchange_type=ExchangeType.topic,durable=True)

    channel.basic_consume('WorkIn',on_message_callback=process_message,auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    main()