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

class HTTPCLientGoldFish(BaseClient):
	'''
	http://rmaqnddj5882.diskn.com/0RkD72oY8j =>미진
	http://rmaqnddj5882.diskn.com/1mBJeR6x80=>주간
	http://rmaqnddj5882.diskn.com/1mBJeR5ruC=>야간
	http://rmaqnddj5882.diskn.com/0Rfw3zBOYD=>마지막
	'''

	url = 'https://www.koreaspot33.com/g5/bbs/board.php?bo_table=profile&wr_id=10060&sca=%EC%95%88%EB%A7%88'
	urlUpdateStamp = 'http://localhost/show369/updatestamp.php'
	patt = r'<img\s+src="(http://rmaqnddj5882.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>'
	contents = ''

	dayimgs = ["1mBJeR6x80"]
	nightimgs = ["1mBJeR5ruC"]
	endimgs = ["0Rfw3zBOYD"]

	cmtiltleimgs = ["0Rfw3zBOYD",  #phone
#					"1mBJeR6x80",  # nightimgs#
#					"1mBJeR5ruC",  # nightimgs
					"36ghEurkvW","1ReOKJf21G","2RVfdCGNCK","2m6Tv7pqC8","0Rfw3zBOYD","0Rlz7xSirO","0Rfw3zBOYD","26rv6Pf4wK","1mDXKwNxe4","36m1lkiB9e","0Rfw3zBOYD","36lVOQOSdO","0Rfw3zBOYD","26t0Cme69S","0Rfw3zBOYD","26uRSmSpwC","0Rfw3zBOYD","0mOTEhBN0G","0Rfw3zBOYD","2RR0RcQS40","0Rfw3zBOYD","36isvL1yb8","0Rfw3zBOYD","171A4SYNlk","0Rfw3zBOYD","1RdasP7Viq","0Rfw3zBOYD","0RkctApf9q","0Rfw3zBOYD","36iE24Bwre","0Rfw3zBOYD","2m4WIxlAhW","0Rfw3zBOYD"]




	def __init__(self,handler=None):
		if handler == None:
			handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')

		self.init('goldfhish',handler)
		print('__init__')
		d = datetime.datetime.now()
		self.dstfile = 'list.' + d.strftime('%Y%m%d') + '.txt'
		print(d.strftime('%Y/%m/%d'))





	def append(self, str):
		self.contents += str
		self.contents += "\r\n"

	def geturlcontents(self):
		r = requests.get(self.url)
		neolib.StrToFile(r.text,'org.html')
		self.availableContets =  self.getAvailabeContents(r.text)

		neolib.StrToFile(self.availableContets, 'avail.html')








	def makecontents(self):

		self.results = re.findall(self.patt, self.availableContets)
		print(self.results)

		self.realarray = []
		self.maparray = {}

		etcinfo = ''
		id = ''

		isavail = False
		self.realarray = []
		for vars in self.results:
			imgsrc, imgid = vars
			if imgid in self.cmtiltleimgs: continue
			print(imgid)
			self.realarray.append(imgid)

		#self.realarray = [vars[1] for vars in self.results if vars[2] == '' or vars[1] in [ self.dayimg ,self.nightimg] ]

		self.ids = ','.join(self.realarray)
		m = hashlib.sha256()
		m.update(self.ids.encode())
		reshash = m.digest()


		self.hashuids = neolib.ByteArray2HexString(reshash)
		self.logger.debug("ids : %s", self.ids)

	def makeProfile(self):
		self.resultsProfile = re.findall(self.pattProfile, self.availableContets)
		self.mapProfile = collections.OrderedDict()
		totalignorimgs = []

		totalignorimgs.extend(self.cmtiltleimgs)
		totalignorimgs.extend(self.startimgs)
		totalignorimgs.append(self.dayimg)
		totalignorimgs.append(self.nightimg)

		for vars in self.resultsProfile:
			imgsrc = vars[0]
			imgid = vars[1]
			imgsrc2 = vars[2]
			imgid2= vars[3]
			title = vars[4]
			if imgid in totalignorimgs: continue
			if imgid2 in totalignorimgs: continue

			self.mapProfile[title] = (imgid,imgid2)




		print(self.mapProfile)
		#self.mapProfile = {vars[2]: (vars[1], "") for vars in self.results if vars[2] != ''}


	def makeTotalContents(self):


		mapFinal = {}

		mapFinal['ids'] = self.realarray
		mapFinal['hashuids'] = self.hashuids
		mapFinal['profile'] = {}


		injson = json.dumps(mapFinal, ensure_ascii=False)
		self.logger.debug("injson : %s", injson)

		self.bencodeProfile = base64.urlsafe_b64encode(injson.encode()).decode()

	# print(self.bencodeProfile)



	def getAvailabeContents(self, str):
		try:
			startIndex = str.index("<!-- 본문 내용 시작 { -->")
			endIndex = str.index("<!-- } 본문 내용 끝 -->")
			return str[startIndex:endIndex]
		except:
			startIndex = -1
			endIndex = -1




		for match in re.finditer(self.patt, str):
			if startIndex < 0 : startIndex = match.span()[0]
			endIndex = match.span()[1]

		return str[startIndex:endIndex]

	def getTodayListBlock(self,str):

		startIndex = 0
		endindex = 0;
		for match in re.finditer(self.pattStartPrfofile, str):
			startIndex = match.span()[1]
		# print(match.span())
		return str[0:startIndex]

	def getProfileBlock(self,str):
		startIndex = 0
		endindex = 0;
		for match in re.finditer(self.pattStartPrfofile, str):
			startIndex = match.span()[1]
			#print(match.span())

		str = str[startIndex:]
		match = re.search(self.pattEndPrfofile, str)

		endindex = match.span()[1]

		#print(str[0:endindex])

		return str[0:endindex]
	def extractProfileMap(self,str):

			str = str.replace("\r", "");
			str = str.replace("\n", "");

			list = re.split(r'<br\s*/\s*>', str)

			rearrstr = '\n'.join(list)

			mapProfile = {}
			for tmp in re.findall(self.pattProfile, rearrstr):
				extprofile = ''
				if (len(tmp) == 4):
					extprofile = tmp[3]
				mapProfile[tmp[1]] = (tmp[0], extprofile)
			return mapProfile




	def updatecontents(self):
		url = self.urlUpdateStamp + '?ids=' + self.ids + '&base64=' + self.bencodeProfile
		#print(url)
		result = requests.get(url)
		self.logger.debug("url : %s res: %s  "%( url,result.text))
		#print(result.text)




	def doRun(self):

		self.logger.info('geturlcontents')
		self.geturlcontents()
		self.logger.info('geturlcontents Done')

		self.logger.info('makecontents')
		self.makecontents()
		self.logger.info('makecontents Done')

		# self.logger.info('makeProfile')
		# self.makeProfile()
		# self.logger.info('makeProfile Done')

		self.logger.info('makeTotalContents')
		self.makeTotalContents()
		self.logger.info('makeTotalContents Done')


		self.logger.info('updatecontents')
		self.updatecontents()
		self.logger.info('updatecontents Done')


		# print(imglist)

	def test(self):
		print('test')
		None

if __name__ == '__main__':
	handleGoldFish = HTTPCLientGoldFish()
	handleGoldFish.Run()
