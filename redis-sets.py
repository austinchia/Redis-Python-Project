# Using Sets and Sorted Sets

# SADD: Add multiple members to a set
r.sadd("tags:python", "redis", "windows", "backend")

# SMEMBERS: Retrieve all unique members in the set
tags = r.smembers("tags:python")
print(tags)  # {b'redis', b'windows', b'backend'}

# Sorted Sets

# ZADD: Add members with scores
r.zadd("leaderboard", {"player1": 10, "player2": 20})

# ZRANGE: Retrieve members in ascending order of score
leaders = r.zrange("leaderboard", 0, -1, withscores=True)
print(leaders)  # [(b'player1', 10.0), (b'player2', 20.0)]

# Managing Tags or Leaderboards

def add_tag(post_id, tag):
    """
    Adds a 'tag' to the set of tags belonging to a specific post.
    Each post has its own set under 'post:{post_id}:tags'.
    """
    r.sadd(f"post:{post_id}:tags", tag)

def get_tags(post_id):
    """
    Retrieves all tags for a specific post, decoding the bytes into strings.
    """
    raw_tags = r.smembers(f"post:{post_id}:tags")
    return {tag.decode('utf-8') for tag in raw_tags}

def update_leaderboard(player, score):
    """
    Updates or inserts a player's score in the 'game:leaderboard' sorted set.
    A higher score indicates a better position if sorting descending.
    """
    r.zadd("game:leaderboard", {player: score})

def get_leaderboard():
    """
    Returns an ascending list of (player, score) tuples from the leaderboard.
    To invert the sorting (highest first), you'd use ZREVRANGE.
    """
    entries = r.zrange("game:leaderboard", 0, -1, withscores=True)
    return [(player.decode('utf-8'), score) for player, score in entries]

# Usage demonstration
add_tag(123, "python")
add_tag(123, "redis")
print(get_tags(123))

update_leaderboard("Alice", 300)
update_leaderboard("Bob", 450)
print(get_leaderboard())
