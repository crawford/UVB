import redis

d = redis.Redis()

def get_username(secret):
	return d.get("secret:" + secret)
	
def increment_kills(username):
	d.hincrby('user:' + username, 'kills', 1)

def increment_steps(username):
	d.hincrby('user:' + username, 'steps', 1)

def increment_deaths(username):
	d.hincrby('user:' + username, 'deaths', 1)
