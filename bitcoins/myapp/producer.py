from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = None


def connect():
    print("connected producer")
    global producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: dumps(x).encode('utf-8'))


def send_producer(message):
    global producer
    if not producer:
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                      value_serializer=lambda x: dumps(x).encode('utf-8'))
    if producer:
        producer.send('bitcoins', value=message)
    else:
        raise Exception("No producer found")