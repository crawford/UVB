#!/usr/bin/python

import logging
import logging.handlers

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

def create_logger(name):
	LOG_FILENAME = '/var/www/test/uvb.log'
	
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	rotHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=5)

	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	rotHandler.setFormatter(formatter)

	logger.addHandler(rotHandler)

	strHandler = logging.StreamHandler()
	strHandler.setLevel(logging.INFO)
	logger.addHandler(strHandler)

	return logger
