import jsonpickle

def dump(objects):
	return jsonpickle.encode(objects)

def load(dump):
	return jsonpickle.decode(dump)
