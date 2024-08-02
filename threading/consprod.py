import random
import threading
import concurrent.futures
import logging
import time
import queue

def producer(queue, event):
    """
    Function that simulates a producer putting messages into a queue.

    Parameters
    ----------
    queue : queue.Queue
        The queue to put messages into.
    event : threading.Event
        The event used to signal when to stop producing messages.
    """
    while not event.is_set():
        # Generate a random message
        message = random.randint(1, 100)
        # Simulate time taken to produce a message
        time.sleep(random.randint(1, 5))
        # Put the message into the queue
        queue.put(message)
        logging.info("Producer put message: %d", message)
    logging.info("Producer received event. Finishing")

def consumer(queue, event):
    """
    Function that simulates a consumer taking messages from a queue.

    Parameters
    ----------
    queue : queue.Queue
        The queue to take messages from.
    event : threading.Event
        The event used to signal when to stop consuming messages.
    """
    while not event.is_set() or not queue.empty():
        # Simulate time taken to consume a message
        time.sleep(random.randint(1, 5))
        # Get a message from the queue
        message = queue.get()
        logging.info("Consumer got message: %d", message)
    logging.info("Consumer received event. Finishing")

if __name__ == "__main__":
    """
    Main function to set up logging, create a queue and event, and run the producer and consumer.
    """
    # Configure logging
    logging.basicConfig(
        format="%(asctime)s : %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    
    # Create a queue with a maximum size of 15
    pipeline = queue.Queue(maxsize=15)
    
    # Create an event to signal when to stop the threads
    event = threading.Event()
    
    # Use ThreadPoolExecutor to manage threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit the producer and consumer functions to the executor
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)
        
        # Allow the producer and consumer to run for 20 seconds
        time.sleep(20)
        
        # Signal the threads to stop
        event.set()

