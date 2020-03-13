import datetime
from datetime import timedelta

import pytz
from celery.task import periodic_task
from django.utils import timezone
from django.core.cache import cache
from celery import shared_task


@shared_task
def write_to_redis(messages):
    print("writing to redis")
    if 'transactions' in cache:
        cache_list = cache.get('transactions')
        for obj in messages:
            cache_list.append(obj)
        cache.set('transactions', cache_list)
    else:
        cache_list = []
        for obj in messages:
            cache_list.append(obj)
        cache.set('transactions', cache_list)


@shared_task
def write_count_of_transactions(key, count):
    print("writing to redis")
    current_time = timezone.now()
    if 'count_of_transactions' in cache:
        cache_dict = cache.get('count_of_transactions')
        result = {key: count}
        cache_dict.update(result)
        cache.set('count_of_transactions', cache_dict)
    else:
        result = {key: count}
        cache.set('count_of_transactions', result)


@periodic_task(run_every=timedelta(hours=3))
def delete_transactions_older_than_3_hours():
    cache_list = cache.get('transactions')
    new_list = []
    for data in cache_list:
        if "x" in data:
            if "time" in data["x"]:
                timestamp = data["x"]["time"]
                if timestamp:
                    date = datetime.datetime.fromtimestamp(timestamp)
                    utc_date = date.replace(tzinfo=pytz.UTC)
                    current_date = timezone.now()
                    if current_date - datetime.timedelta(hours=3) <= utc_date <= current_date:
                        new_list.append(data)
    cache.set('transactions', new_list)