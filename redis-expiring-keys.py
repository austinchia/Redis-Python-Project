# Expiring Keys in Redis

# EXPIRE: Set a 30-second expiration on a key
r.set("temp_key", "some value")
r.expire("temp_key", 30)

# SETEX: Combined set + expire in one command
r.setex("temp_key2", 60, "another value")


# Session expiration

def store_session_with_expiry(user_id, token, ttl=3600):
    """
    Stores a session token for a specific user with a time-to-live (TTL).
    By default, the session expires after 1 hour (3600 seconds).
    """
    session_key = f"user:{user_id}:session"
    r.setex(session_key, ttl, token)

def get_session_with_expiry(user_id):
    """
    Retrieves the session token for the user. Returns None if the key doesn't exist
    or if it has expired.
    """
    session_key = f"user:{user_id}:session"
    token = r.get(session_key)
    return token.decode('utf-8') if token else None

# Usage
store_session_with_expiry(2001, "session_token_abc", 3600)
retrieved_token = get_session_with_expiry(2001)
print(f"Retrieved token: {retrieved_token}")
