from datetime import timedelta

from celery.task import periodic_task
from django.utils import timezone
from django.core.cache import cache
from celery import shared_task

@shared_task
def write_to_redis(obj):
    print("writing to redis")
    current_time = timezone.now()
    result = {'time':current_time, 'obj':obj}
    cache.set(obj['x']['out']['addr'], result, timeout=10800)


@periodic_task(run_every=timedelta(minutes=1))
def write_count_of_transactions():
    print("Running periodic task!")