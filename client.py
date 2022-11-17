import cv2
import numpy as np
import sys
import time

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

# Default RabbitMQ server URI
rabbit_url = 'amqp://guest:guest@localhost:5672//'
import base64
# Kombu Message Consuming Worker
class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['image/jpeg'])]

    def on_message(self, body, message):
        # get the original jpeg byte array size
        imgbin = base64.b64decode(body)
        # # jpeg-encoded byte array into numpy array
        # np_array = np.frombuffer(imgbin, dtype=np.uint8)
        # print(np_array)
        jpg = np.frombuffer(imgbin, dtype=np.uint8)

        # JPEG-decode back into original frame - which is actually a Numpy array
        im = cv2.imdecode(jpg, cv2.IMREAD_UNCHANGED)

        # # decode jpeg-encoded numpy array 
        # # show image
        cv2.imshow("image", im)
        cv2.waitKey(1)

        # send message ack
        message.ack()

def run():
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    with Connection(rabbit_url, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

if __name__ == "__main__":
    run()
