from show369.base_client import *

class HTTPCLient369(BaseClient):
	url = 'https://www.annma.net/g5/bbs/board.php?bo_table=profile&wr_id=141'
	# url = 'https://www.koreaspot33.com/g5/bbs/board.php?bo_table=profile&wr_id=10060&sca=%EC%95%88%EB%A7%88'
	# urlUpdateStamp = 'http://neo1seok.iptime.org/show369/updatestamp.php'
	urlUpdateStamp = 'http://localhost/show369/updatestamp.php'
	patt = r'<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>\s*([^<]*)\s*(?:<\s*br\s*/\s*>)*'
	pattProfile = r'<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>\s*(?:<img\s+src="(http://369am.diskn.com/[a-zA-Z0-9]{8,11})"\s+alt="([a-zA-Z0-9]{8,11})"\s*/>)*\s*([가-힣]+)\s*(?:(?:<\s*br\s*/\s*>\s*)|(?:\s*<\s*/\s*div\s*>\s*))*'

	# pattStartPrfofile = r'<img\s+src="http://369am.diskn.com/1RWbHAyiXm"\s+alt="1RWbHAyiXm"\s* />\s*<\s*br\s*/\s*>'
	# pattEndPrfofile = r'<\s*/\s*div\s*>'
	# pattProfile = r'<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />\s*([가-힣]+)(<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />)*'
	contents = ''
	dayimg = "1RWbHAyiXm";
	nightimg = "1m9RfmwuNy";
	endimgnightimg = "26kx0amYpu";

	startimgs = ["2RUmSzvODG" ,"2RUmSzzYke" ,"26rw4O6dii" ,"36kEwWsZXO"]
	cmtiltleimgs = ["0mMWMdnZH8", "26rl66FLlq", "0mMNVe9jGU", "2m7RtK36ku", "1Rc4IsIr6i", "0RjX72E3cU", "1Rc4Is9Anq", "16zDuGCLf2",	 "26rl669Sk0", "1Rc4IsDBGW", "0mMNVeHhU8", "2m7RtKAy0O", "1mEuhUD6mu", "0RjX72Kdtx", "2RUY9J4jYG"]




	def __init__(self ,handler):
		self.init('show369' ,handler)
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
		neolib.StrToFile(r.text ,'org.html')
		self.availableContets =  self.getAvailabeContents(r.text)

		neolib.StrToFile(self.availableContets, 'avail.html')

	# print(r.text)



	# self.strTodayList = self.getTodayListBlock(r.text)
	# print(self.strTodayList)


	# strprfBlock = self.getProfileBlock(r.text)
	# self.mapProfile = self.extractProfileMap(strprfBlock)






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
			imgsrc, imgid, title = vars
			if imgid in self.cmtiltleimgs: break
			if title != '' and imgid not in [self.dayimg, self.nightimg]: continue
			print(title, imgid)
			self.realarray.append(imgid)

		# self.realarray = [vars[1] for vars in self.results if vars[2] == '' or vars[1] in [ self.dayimg ,self.nightimg] ]

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

			self.mapProfile[title] = (imgid, imgid2)

		print(self.mapProfile)

	# self.mapProfile = {vars[2]: (vars[1], "") for vars in self.results if vars[2] != ''}


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
			if startIndex < 0 :startIndex = match.span()[0]
			endIndex = match.span()[1]

		return str[startIndex:endIndex]

	def getTodayListBlock(self,str ):

		startIndex = 0
		endindex = 0;
		for match in re.finditer(self.pattStartPrfofile, str):
			startIndex = match.span()[1]
		# print(match.span())
		return str[0:startIndex]

	def getProfileBlock(self,str ):
		startIndex = 0
		endindex = 0;
		for match in re.finditer(self.pattStartPrfofile, str):
			startIndex = match.span()[1]
		# print(match.span())

		str = str[startIndex:]
		match = re.search(self.pattEndPrfofile, str)

		endindex = match.span()[1]

		# print(str[0:endindex])

		return str[0:endindex]
	def extractProfileMap(self,str ):

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
		# print(url)
		result = requests.get(url)
		self.logger.debug("url : %s res: %s  "%( url, result.text))

	# print(result.text)




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

