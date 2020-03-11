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


def connect_consumer():
    start_timer()
    consumer = KafkaConsumer(
        'bitcoins',
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         enable_auto_commit=True,
         group_id='my-group',
         value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        count = count + 1
        message = message.value
        print(message)


def start_timer():
    schedule.every(10).minutes.do(write_to_redis)
    while True:
        schedule.run_pending()
        time.sleep(1)


def write_to_redis():
    if 'product' in cache:
        # get results from cache
        result = cache.get('count_of_transactions')
        time = str(hours) + ":" + str(minutes)
        result.append({time : count})
        result.append(result)
    else:
        time = str(hours) + ":" + str(minutes)
        dict = {time:count}
        new_list = [dict]
        cache.set('count_of_transactions', time + new_list, timeout=3600)