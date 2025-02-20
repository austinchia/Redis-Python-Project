# Redis Features in Python Applications

# 1. Redis as a Queue (with Blocking)
def blocking_consumer(queue_name):
    """
    Continuously listens to the specified queue (Redis list) using BLPOP,
    which blocks until new items are pushed. Once an item arrives,
    it is removed from the queue and processed.
    """
    print(f"Waiting on queue: {queue_name}")
    while True:
        result = r.blpop(queue_name)
        if result:
            list_name, task_bytes = result
            task = task_bytes.decode('utf-8')
            print(f"Received task: {task}")
        else:
            print("Queue is empty or an error occurred.")
            break

def enqueue_task(queue_name, task):
    """
    Pushes a task to the end of a Redis list (queue).
    """
    r.rpush(queue_name, task)

# Example usage:
enqueue_task("blocking_queue", "task_block_1")
enqueue_task("blocking_queue", "task_block_2")

# In a real application, the consumer might run in a separate thread or process
blocking_consumer("blocking_queue")

# 2.Implementing Locks in Redis

import time
from redis.exceptions import LockError

def process_critical_section():
    """
    Acquires a lock named 'resource_lock' with a timeout of 10 seconds.
    The lock automatically expires after 10 seconds to prevent deadlocks.
    """
    lock = r.lock("resource_lock", timeout=10)
    try:
        # Attempt to acquire the lock, wait for up to 5 seconds if another process holds it
        acquired = lock.acquire(blocking=True, blocking_timeout=5)
        if acquired:
            print("Lock acquired; performing critical operation...")
            time.sleep(3)  # Simulate some operation
        else:
            print("Failed to acquire lock within 5 seconds.")
    except LockError:
        print("A LockError occurred, possibly releasing already released lock.")
    finally:
        # Always release the lock in a finally block to ensure cleanup
        lock.release()
        print("Lock released.")

# Usage demonstration
process_critical_section()

# 3. Caching with Redis
import requests
import json

def get_user_data(user_id):
    """
    Retrieves user data from a hypothetical API endpoint.
    If the data is found in Redis (cache), use that. Otherwise, call the API,
    store the response in Redis with a 60-second expiration, and return it.
    """
    cache_key = f"user_data:{user_id}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("Cache hit!")
        return json.loads(cached_data)

    print("Cache miss. Fetching from API...")
    response = requests.get(f"https://api.example.com/users/{user_id}")
    user_info = response.json()

    # Store in Redis for 60 seconds
    r.setex(cache_key, 60, json.dumps(user_info))
    return user_info

# Usage
user = get_user_data(42)  # First call => cache miss
user_again = get_user_data(42)  # Subsequent call => cache hit
