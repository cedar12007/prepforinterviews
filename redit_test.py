from upstash_redis import Redis

redis = Redis(url="https://tops-sparrow-26652.upstash.io", token="xxx")

redis.set("foo", "bar")
value = redis.get("foo")

print("value: " + value)
