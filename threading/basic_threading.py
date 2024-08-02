import time
import random
import logging
import threading
import concurrent.futures

class ReaderWriter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    def update(self, index):
        logging.info("thread %d: starting update", index)
        local = self.value
        local += 1
        time.sleep(random.randint(1, 5))
        self.value = local
        logging.info("datapool value: %d", self.value)
        logging.info("thread %d, update completed", index)
    def update_with_lock(self, index):
        with self.lock:
            self.update(index)

def worker(index):
    logging.info("thread %d is starting", index)
    time.sleep(random.randint(1, 5))
    logging.info("thread %d has finished", index)

def example1():
    logging.info("main thread: starting")
    threads = []
    for index in range(10):
        t = threading.Thread(target=worker, args=(index,))
        threads.append(t)
        t.start()
    logging.info("main thread: waiting workers to finish")
    for t in threads:
        t.join()
    logging.info("main thread: done")

def example2():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(worker, range(10))

def example3():
    datapool = ReaderWriter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for index in range(10):
            executor.submit(datapool.update, index)

def example4():
    datapool = ReaderWriter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for index in range(10):
            executor.submit(datapool.update_with_lock, index)

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    logging.info("### Example 1: Loop to launch threads ###")
    example1()
    logging.info("### Example 2: Pool executor ###")
    example2()
    logging.info("### Example 3: Race condition ###")
    example3()
    logging.info("### Example 4: Lock to avoid race condition ###")
    example4()
