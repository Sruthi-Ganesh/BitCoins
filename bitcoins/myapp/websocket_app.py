import websocket
from myapp.producer import send_producer

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    print(message)
    send_producer(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        ws.send("{\"op\":\"ping\"}")
        ws.send("{\"op\":\"unconfirmed_sub\"}")
        print("thread terminating...")
    thread.start_new_thread(run, ())


def connect():
    print("connected websocket")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()