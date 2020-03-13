import datetime
import operator

import pytz
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache


class TransactionView(APIView):
    def get(self, request, format=None):
        cache_list = cache.get('transactions')
        trunc_list = cache_list[-100:]
        return Response(trunc_list)


class CountOfTransactionView(APIView):
    def get(self, request, min_value, format=None):
        cache_dict = cache.get('count_of_transactions')
        min_value_list = []
        for key in cache_dict:
            value = cache_dict[key]
            print(key)
            print(value)
            if value >= min_value:
                min_value_list.append({key:value})
        return Response(min_value_list)


class AddressView(APIView):
    def get(self, request, format=None):
        cache_list = cache.get('transactions')
        addr = {}
        if cache_list:
            for data in cache_list:
                if 'x' in data:
                    sub_data = data['x']
                    if 'time' in sub_data:
                        timestamp = sub_data["time"]
                        date = datetime.datetime.fromtimestamp(timestamp)
                        utc_date = date.replace(tzinfo=pytz.UTC)
                        current_date = timezone.now()
                        if current_date - datetime.timedelta(hours=3) <= utc_date <= current_date:
                            if 'out' in sub_data:
                                if len(sub_data['out']) > 0:
                                    for address in sub_data['out']:
                                        print(address)
                                        if address["addr"]:
                                            if address["addr"] in addr:
                                                count = addr[address["addr"]]
                                                count = count + 1
                                                addr[address["addr"]] = count
                                            else:
                                                addr[address["addr"]] = 1
        sorted_addr = dict(sorted(addr.items(), key=operator.itemgetter(1),reverse=True))
        return Response(sorted_addr)
