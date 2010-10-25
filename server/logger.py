import logging
import logging.handlers
import ConfigParser

'''
Instructions:
	from logger import *

	logger = createLogger('your module name')

	logger.debug('message')
	logger.info('message')
	logger.warn('message')
	logger.error('message')
	logger.critical('message')

	The minimum logging levels for file logging and screen logging are below
'''

def init_logger(config_file):
	config = ConfigParser.ConfigParser()
	config.read(config_file)

	LOG_FILENAME = config.get('Server', 'Log')

	logger = logging.getLogger('')
	rotHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=5)

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	rotHandler.setFormatter(formatter)

	logger.addHandler(rotHandler)
	
	strHandler = logging.StreamHandler()
	strHandler.setLevel(logging.WARN)

	logger.addHandler(strHandler)


def create_logger(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)

	return logger
