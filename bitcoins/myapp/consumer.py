import json
import time
import datetime
import pytz
import schedule
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from kafka import KafkaConsumer
from json import loads
from django.core.cache import cache
count = 0
hours = 1
minutes = 0
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
consumer = None
from django.utils import timezone
import threading
from myapp.tasks import write_to_redis, write_count_of_transactions
messages = []

def connect():
    print("connected consumer")
    global consumer, count, messages
    consumer = KafkaConsumer(
        'bitcoins',
        bootstrap_servers=['localhost:9092'],
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.poll()
    consumer.seek_to_end()

    threading.Timer(60.0, set_count_to_cache).start()
    for message in consumer:
        count = count + 1
        message = message.value
        obj = json.loads(message)
        timestamp = obj["x"]["time"] if obj["x"] else None
        if timestamp:
            date = datetime.datetime.fromtimestamp(timestamp)
            utc_date = date.replace(tzinfo=pytz.UTC)
            current_date = timezone.now()
            if current_date - datetime.timedelta(hours=3) <= utc_date <= current_date:
                messages.append(obj)



def set_count_to_cache():
    print("set count to cache called")
    global minutes, count, messages
    threading.Timer(60.0, set_count_to_cache).start() # called every minute
    if minutes == 59:
        minutes = 0
    else:
        minutes = minutes + 1
    key_string = str(hours) + ":" + str(minutes)
    print("calling count of transactions")
    write_count_of_transactions.delay(key_string, count)
    write_to_redis.delay(messages)
    messages = []
    count = 0
