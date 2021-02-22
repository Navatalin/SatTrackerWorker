from numpy import true_divide
import pika
from pika.exchange_type import ExchangeType
import jsons
from Tracking import Tracking
import redis
import base64


tracking = Tracking()

def process_message(body):
    sat_names = jsons.loads(body)
    tracking.get_pos(sat_names)

def main():
    r = redis.Redis(host='localhost',port=6379, db=0)
    r_channel = r.pubsub()
    r_channel.subscribe('WorkIn')
    r_channel.get_message()

    while(True):
        message = r_channel.get_message()
        if message:
            if(message.get('type') != 'subscribe'):
                data = bytearray(message.get('data'))
                process_message(data.decode())


if __name__ == '__main__':
    main()