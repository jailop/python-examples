import random
import threading
import concurrent.futures
import logging
import time
import queue

def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 100)
        time.sleep(random.randint(1, 5))
        queue.put(message)
        logging.info("Producer put message: %d", message)
    logging.info("Producer received event. Finishing")

def consumer(queue, event):
    while not event.is_set() or not queue.empty():
        time.sleep(random.randint(1, 5))
        message = queue.get()
        logging.info("Consumer got message: %d", message)
    logging.info("Consumer received event. Finishing")

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    pipeline = queue.Queue(maxsize=15)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)
        time.sleep(20)
        event.set()
