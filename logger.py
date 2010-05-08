#!/usr/bin/python

import logging
import logging.handlers

def createLogger(name):
	LOG_FILENAME = 'uvb.log'
	
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
