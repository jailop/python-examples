import zmq
import json
import time
from multiprocessing import Process, Manager
import localnet

def receiver(queue):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:51230")
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    while True:
        message = socket.recv()
        data = json.loads(message.decode())
        queue.put(data['time'])

class PingManager:
    def __init__(self, target):
        self.target = target
        self.pub = None
        self.sub = None
        m = Manager()
        self.queue = m.Queue()
        self.running = False
    def start(self):
        self.pub = Process(target=localnet.ping, args=(self.target,))
        self.sub = Process(target=receiver, args=(self.queue,))
        self.pub.start()
        self.sub.start()
        self.running = True
    def get(self):
        return self.queue.get()
    def stop(self):
        if self.pub:
            self.running = False
            self.sub.terminate()
            self.sub = None
            self.pub.terminate()
            self.pub = None

if __name__ == '__main__':
    pm = PingManager('192.168.88.1')
    pm.start()
    for i in range(10):
        print(i, pm.get())
    pm.stop()
