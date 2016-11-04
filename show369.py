import re
import requests
import datetime
import shutil
import sys
import time
import gc
import  json

import codecs
import base64

class HTTPCLient369():
	url = 'https://www.annma.net/g5/bbs/board.php?bo_table=profile&wr_id=141'
	urlUpdateStamp = 'http://localhost/show369/updatestamp.php'
	patt = r'<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>'

	pattStartPrfofile = r'<img\s+src="http://369am.diskn.com/1RWbHAyiXm"\s+alt="1RWbHAyiXm"\s* />\s*<\s*br\s*/\s*>'
	pattEndPrfofile = r'<\s*/\s*div\s*>'
	pattProfile = r'<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />\s*([가-힣]+)(<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />)*'
	contents = ''
	dayimg = "1RWbHAyiXm";
	nightimg = "1m9RfmwuNy";
	endimgnightimg = "26kx0amYpu";



	def __init__(self):
		print('__init__')
		d = datetime.datetime.now()
		self.dstfile = 'list.' + d.strftime('%Y%m%d') + '.txt'
		print(d.strftime('%Y/%m/%d'))

	def __del__(self):
		gc.collect()
		print('__del__')




	def append(self, str):
		self.contents += str
		self.contents += "\r\n"

	def geturlcontents(self):
		r = requests.get(self.url)
		self.availableContets =  self.getAvailabeContents(r.text)

		print(self.availableContets)



		self.strTodayList = self.getTodayListBlock(r.text)
		#print(self.strTodayList)
		self.results = re.findall(self.patt, self.availableContets)


		strprfBlock = self.getProfileBlock(r.text)
		self.mapProfile = self.extractProfileMap(strprfBlock)






	def makecontents(self):

		self.realarray = []
		self.maparray = {}

		etcinfo = ''
		id = ''

		isavail = False

		for vars in self.results:
			id = vars[1]
			srcname = vars[0]

			self.maparray[id] = srcname;
			if id == self.dayimg:
				isavail = True
			if id == self.endimgnightimg:
				self.realarray.append(id)
				break;

			if isavail:
				self.realarray.append(id)

		self.ids = ''
		for key in self.realarray:
			id = key
			self.ids += id
			self.ids += ','

		mapFinal = {}

		mapFinal['ids'] = self.realarray
		mapFinal['profile'] = self.mapProfile



		injson = json.dumps(mapFinal,ensure_ascii=False)
		print(injson)

		self.bencodeProfile = base64.urlsafe_b64encode(injson.encode()).decode()
		#print(self.bencodeProfile)

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
		print(url)
		result = requests.get(url)
		print(result.text)




	def doRun(self):

		self.geturlcontents()

		self.makecontents()

		self.updatecontents()


		# print(imglist)

	def test(self):
		print('test')
		None

class GetLateestWebtoon():
	webtoonurlfmt = "http://comic.naver.com/webtoon/list.nhn?titleId={0}"
	urlGetTodayWebToon = "http://localhost/webtoon/webtoon.php?option=todaylist"
	urlGetAllWebToon = "http://localhost/webtoon/webtoon.php?option=alllist"
	urlUpdateTopIds = "http://localhost/webtoon/webtoon.php?option=updatetopids"


	def __init__(self):
		print('GetLateestWebtoon')


	def __del__(self):
		gc.collect()
		print('__del__')


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

	def doRun(self,isAll):
		mapTopid = {}
		url = self.urlGetTodayWebToon
		if isAll == 'true':
			url = self.urlGetAllWebToon

		self.getList(url)
		for key in self.todaylist:
			value = self.getTopId(key)
			mapTopid[key] = value
		injson = json.dumps(mapTopid)
		print(injson)

		bencode = base64.urlsafe_b64encode(injson.encode()).decode()
		print(bencode)
		
		url = self.urlUpdateTopIds + "&json=" + bencode
		print(url)
		r = requests.get(url)
		print(r.text)




		# print(imglist)

	def test(self):
		print('test')
		None

if __name__ != '__main__':
	exit()

#GetLateestWebtoon().doRun_test()
#exit()

dstpath = ''
waittime = 20
takentime = 1
maxtime = 1;
unittile = 10;
isAll = 'false'
if len(sys.argv) > 1:
	dstpath = sys.argv[1]
	print(sys.argv[1])

if len(sys.argv) > 2:
	waittime = int(sys.argv[2])

	maxtime = waittime * 60
	print(waittime)

if len(sys.argv) > 3:
	isAll = sys.argv[3]

print("datpath:{0} \r\nwaittime:{1} min".format(dstpath,waittime))


#HTTPCLient369().doRun()
#exit()
takentime = waittime * 60 + 1;

log = ''



while True:

	if takentime> maxtime:
		log = "{0} tktime:{1} doRun \n".format(datetime.datetime.now().isoformat(), 0)
		try:
			HTTPCLient369().doRun()
		except :
			log += "{0} HTTPCLient369 ValueError:{1}  \n".format(datetime.datetime.now().isoformat(), 0)



		try:
			GetLateestWebtoon().doRun(isAll)
		except  :
			log += "{0} GetLateestWebtoon ValueError:{1}  \n".format(datetime.datetime.now().isoformat(), 0)

		takentime = 0

	print(log);
	f = open("out.log", 'ab')
	f.write(log.encode())
	f.close()

	time.sleep(unittile)
	takentime += unittile;
	log = "{0} tktime:{1} \n".format(datetime.datetime.now().isoformat(), takentime)


