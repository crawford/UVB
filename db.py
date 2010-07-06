import redis

d = redis.Redis()

def get_username(secret):
	return d.get("secret:" + secret)
