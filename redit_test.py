from upstash_redis import Redis

redis = Redis(url="https://tops-sparrow-26652.upstash.io", token="AWgcAAIjcDFlMzk4NzI1MTQ0MDA0NTY0ODRlNjMwN2Y3ZDJhMDcwZXAxMA")

redis.set("foo", "bar")
value = redis.get("foo")

print("value: " + value)
