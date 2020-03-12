from django.apps import AppConfig
from myapp import producer, websocket_app, consumer


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        print('My app')
        # print("connecting web socket")
        # websocket_app.connect()
        # producer.connect()
        # consumer.connect()

