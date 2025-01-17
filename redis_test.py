from upstash_redis import Redis

# Initialize the Redis client
redis_client = Redis(
    url="https://tops-sparrow-26652.upstash.io",  # Replace with your Upstash Redis URL
    token="xxx"             # Replace with your Upstash token
)

# Test the connection
try:
    redis_client.set("test_key", "Hello, Upstash!")
    value = redis_client.get("test_key")
    print(f"Value from Redis: " + str(value))
except Exception as e:
    print(f"Error connecting to Upstash Redis: {e}")
