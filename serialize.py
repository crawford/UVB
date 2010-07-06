import simplejson

def dump(objects):
	return simplejson.dumps(objects)

def load(dump):
	return simplejson.loads(dump)