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





class HTTPCLient369(BaseClient):
	url = 'https://www.annma.net/g5/bbs/board.php?bo_table=profile&wr_id=141'
	#urlUpdateStamp = 'http://neo1seok.iptime.org/show369/updatestamp.php'
	urlUpdateStamp = 'http://localhost/show369/updatestamp.php'
	patt = r'<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>\s*([^<]*)\s*(?:<\s*br\s*/\s*>)*'
	pattProfile = r'<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>\s*(?:<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>)*\s*([가-힣]+)\s*(?:(?:<\s*br\s*/\s*>\s*)|(?:\s*<\s*/\s*div\s*>\s*))*'

	#pattStartPrfofile = r'<img\s+src="http://369am.diskn.com/1RWbHAyiXm"\s+alt="1RWbHAyiXm"\s* />\s*<\s*br\s*/\s*>'
	#pattEndPrfofile = r'<\s*/\s*div\s*>'
	#pattProfile = r'<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />\s*([가-힣]+)(<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />)*'
	contents = ''
	dayimg = "1RWbHAyiXm";
	nightimg = "1m9RfmwuNy";
	endimgnightimg = "26kx0amYpu";

	startimgs = ["2RUmSzvODG","2RUmSzzYke","26rw4O6dii","36kEwWsZXO"]
	cmtiltleimgs = ["0mMWMdnZH8", "26rl66FLlq", "0mMNVe9jGU", "2m7RtK36ku", "1Rc4IsIr6i", "0RjX72E3cU", "1Rc4Is9Anq", "16zDuGCLf2",	 "26rl669Sk0", "1Rc4IsDBGW", "0mMNVeHhU8", "2m7RtKAy0O", "1mEuhUD6mu", "0RjX72Kdtx", "2RUY9J4jYG"]




	def __init__(self,handler):
		self.init('show369',handler)
		print('__init__')
		d = datetime.datetime.now()
		self.dstfile = 'list.' + d.strftime('%Y%m%d') + '.txt'
		print(d.strftime('%Y/%m/%d'))

	# def __del__(self):
	# 	gc.collect()
	# 	print('__del__')




	def append(self, str):
		self.contents += str
		self.contents += "\r\n"

	def geturlcontents(self):
		r = requests.get(self.url)
		neolib.StrToFile(r.text,'org.html')
		self.availableContets =  self.getAvailabeContents(r.text)

		neolib.StrToFile(self.availableContets, 'avail.html')

		#print(r.text)



		#self.strTodayList = self.getTodayListBlock(r.text)
		#print(self.strTodayList)


		#strprfBlock = self.getProfileBlock(r.text)
		#self.mapProfile = self.extractProfileMap(strprfBlock)






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
			imgsrc,imgid,title = vars
			if imgid in self.cmtiltleimgs: break
			if title != '' and imgid not in [ self.dayimg ,self.nightimg]:continue
			print(title,imgid)
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
		mapFinal['profile'] = self.mapProfile


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

		self.logger.info('makeProfile')
		self.makeProfile()
		self.logger.info('makeProfile Done')

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

class GetLateestWebtoon(BaseClient):
	webtoonurlfmt = "http://comic.naver.com/webtoon/list.nhn?titleId={0}"
	urlGetTodayWebToon = "http://localhost/webtoon/webtoon.php?option=todaylist"
	urlGetAllWebToon = "http://localhost/webtoon/webtoon.php?option=alllist"
	urlUpdateTopIds = "http://localhost/webtoon/webtoon.php?option=updatetopids"
	isAll = True

	def __init__(self,handler):
		self.init('webtoon',handler)
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



	def getTopId(self,id):

		print(id)


		r = requests.get(self.webtoonurlfmt.format(id))



		startstgtr = '<td class="title">'
		index = r.text.index(startstgtr)
		str = r.text[index:]
		#print(str)
		regexp = r"/webtoon/detail.nhn\?titleId=" + id + r"&no=(\d{1,4}).*"
		regexpniewno = r">(.*)</a>"

		results = re.search(regexp, str)
		str = results.group(0)

		results2 = re.search(regexpniewno, str)


		#print(results.group(1))
		#print(results2.group(1))
		return (results.group(1),results2.group(1))




	def getList(self,url):

		r = requests.get(url)
		print(r.text.encode());
		contents =  r.text.replace(codecs.BOM_UTF8.decode(), "")
		print(contents.encode());
		self.todaylist =  json.loads(contents)


		None






	def updatecontents(self):
		print(self.urlUpdateStamp +'?ids=' +self.ids)
		result = requests.get(self.urlUpdateStamp +'?ids=' +self.ids)
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
		#print(injson)

		bencode = base64.urlsafe_b64encode(injson.encode()).decode()
		#print(bencode)
		
		url = self.urlUpdateTopIds + "&json=" + bencode
		#print(url)
		r = requests.get(url)
		print(r.text)
		self.logger.debug("url:{0} ret:{1}".format(url,r.text))

		self.logger.info('update list Done')




		# print(imglist)

	def test(self):
		print('test')
		None

class LoopProcess(BaseClient):
	waittime = 20
	takentime = 1
	maxtime = 1;
	unittime = 10;
	version = 1.0

	def __init__(self,waittime,unittime):
		super(LoopProcess, self).__init__('LoopProcess')

		self.waittime = waittime
		self.unittime =unittime
		self.logger.info("LoopProcess waittime:{0} min VER:{1}".format(waittime,self.version))


	def getCurTime(self):
		return time.time()
	def doRun(self):

		self.maxtime = self.waittime * 60
		self.takentime = self.maxtime+1
		handle369 = HTTPCLient369(self.handler)
		handleebtoon = GetLateestWebtoon(self.handler)

		listHandler = [handle369,handleebtoon]
		start = -1*self.maxtime;
		while True:

			self.takentime = self.getCurTime() - start;
			#self.logger.debug("%d %d %d",self.getCurTime(),self.takentime,start)
			self.logger.debug("LOOP VER:{2} tktime:{0} {1} ".format(self.takentime, self.maxtime,self.version))

			if self.takentime > self.maxtime:
				start = self.getCurTime()
				for tmp in listHandler:
					try:
						self.logger.info("RUN CLASSNAME:{0} ".format(tmp.__class__))
						tmp.Run();
					except:
						self.logger.debug("{0}  ValueError:{1}  \n".format(tmp.__name__,0))
				continue

			time.sleep(self.unittime)



if __name__ != '__main__':
	exit()
maparg = neolib.getMapsFromArgs(sys.argv)
#GetLateestWebtoon().doRun_test()
#exit()


waittime = 0.1
takentime = 1
maxtime = 1;
unittime = 10;
isAll = 'false'
print(maparg.keys())
if 'waittime' in maparg.keys() :
	waittime = int(maparg['waittime'])

if 'unittime' in maparg.keys() :
	unittime = int(maparg['unittime'])



LoopProcess(waittime,unittime).Run()
#HTTPCLient369().doRun()
#exit()



log = ''






