import time
import signal
import zmq
import json
from multiprocessing import Process
from scapy.all import conf, sr1, IP, ICMP
from rich import print

TIMEOUT = 2
INTERVAL = 1

def ping(target):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:51230")
    while True:
        start = time.time()
        packet = IP(dst=target)/ICMP()
        reply = sr1(packet, timeout=TIMEOUT, verbose=False)
        response = {
            'host': target,
            'time': float('nan'),
            'units': 'ms'
        }
        if reply:
            response['time'] = (reply.time - start) * 1000
        socket.send(json.dumps(response).encode())
        time.sleep(INTERVAL)

def managed_ping(target, num=10):
    p = Process(target=ping, args=(target,))
    p.start()
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:51230")
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    for i in range(num):
        message = socket.recv()
        print(json.loads(message.decode()))
    p.terminate()

def default_connection():
    for route in conf.route.routes:
        if route[0] == 0 and route[1] == 0:
            return {
                'device': route[3],
                'address': route[4],
                'gateway': route[2],
            } 

if __name__ == '__main__':
    conn = default_connection()
    print(conn)
    managed_ping(conn['gateway'])
