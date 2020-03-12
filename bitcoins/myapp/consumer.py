import json
import time
import schedule
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from kafka import KafkaConsumer
from json import loads
from django.core.cache import cache
count = 0
hours = 0
minutes = 0
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
consumer = None
from django.utils import timezone


def connect():
    print("connected consumer")
    global consumer, count
    consumer = KafkaConsumer(
        'bitcoins',
        bootstrap_servers=['localhost:9092'],
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        count = count + 1
        message = message.value
        obj = json.loads(message)
        write_to_redis(obj)
        # print(message)


def start_timer():
    print("started timer")
    schedule.every(1).minutes.do(write_to_redis)
    while True:
        print("running pending")
        schedule.run_pending()
        time.sleep(1)


def write_to_redis(obj):
    print("writing to redis")
    current_time = timezone.now()
    result = {'time':current_time, 'obj':obj}
    cache.set(obj['x']['out']['addr'], result, timeout=10800)
