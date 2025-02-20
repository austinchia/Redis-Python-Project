# LPUSH: Push an element to the head (left) of the list
r.lpush("task_queue", "task1")

# RPUSH: Push an element to the tail (right) of the list
r.rpush("task_queue", "task2")
r.rpush("task_queue", "task3")

# LPOP: Pop (remove and return) the element at the head
task = r.lpop("task_queue")
print(task)  # b'task1'

# Optional: RPOP removes and returns the element at the tail
task = r.rpop("task_queue")
print(task)  # b'task3'


# Implementing a Simple Redis-Backed Queue
def enqueue_task(queue_name, task):
    """
    Appends a task to the end (right) of the Redis list named `queue_name`.
    """
    r.rpush(queue_name, task)

def dequeue_task(queue_name):
    """
    Removes a task from the front (left) of the Redis list named `queue_name`.
    Returns the task as a string, or None if the queue is empty.
    """
    task = r.lpop(queue_name)
    return task.decode('utf-8') if task else None

# Example usage:
enqueue_task("my_queue", "send_email")
enqueue_task("my_queue", "generate_report")

while True:
    task = dequeue_task("my_queue")
    if not task:
        print("No more tasks in queue.")
        break
    print(f"Processing task: {task}")
