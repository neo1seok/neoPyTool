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
import neolib.neolib as neolib

import hashlib
from show_daily_info.base_client import *

class GetLateestWebtoon(BaseClient):
	webtoonurlfmt = "http://comic.naver.com/webtoon/list.nhn?titleId={0}"
	urlGetTodayWebToon = "http://localhost/webtoon/webtoon.php?option=todaylist"
	urlGetAllWebToon = "http://localhost/webtoon/webtoon.php?option=alllist"
	urlUpdateTopIds = "http://localhost/webtoon/webtoon.php?option=updatetopids"
	isAll = True

	def __init__(self, handler):
		self.init('webtoon', handler)
		print('GetLateestWebtoon')

	#
	# def __del__(self):
	# 	gc.collect()
	# 	print('__del__')


	def reff(self):
		id = '409629'
		nicklist = requests.get("http://comic.naver.com/webtoon/list.nhn?titleId={0}".format(id))
		print(nicklist.text)

		startstgtr = '<td class="title">'
		index = nicklist.text.index(startstgtr)
		str = nicklist.text[index:]
		regexp = r"/webtoon/detail.nhn\?titleId=" + id + r"&no=(\d{1,4}).*"
		results = re.search(regexp, str)
		print(results.group(1))

		str = '["foo", {"bar":["baz", null, 1.0, 2]}]'

		safdsf = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
		fsdf = json.loads(safdsf)

	def getTopId(self, id):

		print(id)

		r = requests.get(self.webtoonurlfmt.format(id))

		startstgtr = '<td class="title">'
		index = r.text.index(startstgtr)
		str = r.text[index:]
		# print(str)
		regexp = r"/webtoon/detail.nhn\?titleId=" + id + r"&no=(\d{1,4}).*"
		regexpniewno = r">(.*)</a>"

		results = re.search(regexp, str)
		str = results.group(0)

		results2 = re.search(regexpniewno, str)

		# print(results.group(1))
		# print(results2.group(1))
		return (results.group(1), results2.group(1))

	def getList(self, url):

		r = requests.get(url)
		print(r.text.encode());
		contents = r.text.replace(codecs.BOM_UTF8.decode(), "")
		print(contents.encode());
		self.todaylist = json.loads(contents)

		None

	def updatecontents(self):
		print(self.urlUpdateStamp + '?ids=' + self.ids)
		result = requests.get(self.urlUpdateStamp + '?ids=' + self.ids)
		print(result.text)

	def doRun_test(self):
		self.doRun('true')
		value = self.getTopId('22897');

	def doRun(self):
		mapTopid = {}
		url = self.urlGetTodayWebToon
		if self.isAll == 'true':
			url = self.urlGetAllWebToon

		self.logger.info('getList')
		self.getList(url)
		self.logger.info('getList Done')

		self.logger.info('update list')
		for key in self.todaylist:
			value = self.getTopId(key)
			mapTopid[key] = value
		injson = json.dumps(mapTopid)
		# print(injson)

		bencode = base64.urlsafe_b64encode(injson.encode()).decode()
		# print(bencode)

		url = self.urlUpdateTopIds + "&json=" + bencode
		# print(url)
		r = requests.get(url)
		print(r.text)
		self.logger.debug("url:{0} ret:{1}".format(url, r.text))

		self.logger.info('update list Done')

	# print(imglist)

	def test(self):
		print('test')
		None