# Using Pub/Sub with Redis

import threading

def subscriber(r, channel_name):
    """
    Subscribes to the given Redis channel and listens for messages.
    When a new message is published on that channel, it is printed.
    """
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)
    print(f"Subscribed to {channel_name}")

    # pubsub.listen() yields messages from the subscribed channel(s) in real time
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")

def publisher(r, channel_name, message):
    """
    Publishes a message to the specified Redis channel.
    All subscribers to this channel immediately receive the message.
    """
    r.publish(channel_name, message)

# Example usage
channel = "updates"

# Start subscriber in a separate thread to avoid blocking the main thread
sub_thread = threading.Thread(target=subscriber, args=(r, channel))
sub_thread.start()

# Publish messages
publisher(r, channel, "Hello from Windows!")
publisher(r, channel, "Another update!")
