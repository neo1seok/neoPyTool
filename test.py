import base64
import glob
import gzip
import hashlib
import http.client
import os
import re
import shutil
import socket
import sys
import win32api
import win32gui
import inspect
import requests
import  simplejson as json
import win32con

import neolib.neolib as neolib


#import test.sample


import xlrd


class TestClass:

	aab = ''
	def test(self):
		None
	def test2(self):
		None
	def test3(self,a,c,d):
		None

	def Show(self,a,b,c):
		sig = inspect.signature(self.Show)
		print(str(sig))
		# args, _, _, values = inspect.getargvalues(frame)
		# print(args)
		# print(dir(self))
		# method_list = [func for func in dir(self) if callable(getattr(self, func))]
		# print(method_list)
		None

import urllib.request



exit()
print(re.match(r'asdsa',"adsaf"))

print( globals()['TestClass'])

TestClass().Show(1,2,3)

exit()

print(int('ff', 16))

exit()
klass = globals()["Test"]
instance = klass()
r = requests.get("http://purryfwends.com/article/240/Graphic/warning-graphic-content-naked-man-attempts-suicide-by-lion-cage-turtle-chopped-in-half-revenge-bites-man-compilation")
print(r.text)

import logging
from logging import handlers





handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')


# create logger
logger = logging.getLogger('show369')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
handler.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(handler)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

import test.sample
print(b'aabb')
exit()
