import re
import requests
import datetime
import shutil
import sys
import time
import gc
import  json
import time
import codecs
import base64
import logging
import collections
from logging import handlers
import neolib.neoutil as neolib

import hashlib


class BaseClient():
	def __init__(self,loggename):
		#self.init(loggename)

		self.handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
		self.init(loggename,self.handler)
		#self.logger = self.createLogger(loggename, self.handler)


	def init(self,loggename,handler):
		self.logger = self.createLogger(loggename,handler)

		# self.loggename =loggename
		# # create logger
		# self.logger = logging.getLogger(loggename)
		# self.logger.setLevel(logging.DEBUG)
		#
		# # create console handler and set level to debug
		# ch = logging.StreamHandler()
		# ch.setLevel(logging.DEBUG)
		#
		# # create formatter
		# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		#
		# # add formatter to ch
		# ch.setFormatter(formatter)
		# handler.setFormatter(formatter)
		# # add ch to logger
		# self.logger.addHandler(ch)
		# self.logger.addHandler(handler)

		self.logger.debug("%s __init__", self.__class__.__name__)

	def createLogger(self,loggename,handler):

		#handler = handlers.TimedRotatingFileHandler(filename=loggename + ".txt", when='D')
		self.loggename = loggename
		# create logger
		self.logger = logging.getLogger(loggename)
		self.logger.setLevel(logging.DEBUG)

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# create formatter
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		# add formatter to ch
		ch.setFormatter(formatter)
		handler.setFormatter(formatter)
		# add ch to logger
		self.logger.addHandler(ch)
		self.logger.addHandler(handler)
		return self.logger


	def doRun(self):
		None

	def procExcept(self,ex):
		print(ex)
		self.logger.debug("except:%s",ex)
		None
	def Run(self):
		try:
			self.logger.debug("%s Run", self.__class__.__name__)
			self.doRun()
		except Exception as ex:
			self.procExcept(ex)