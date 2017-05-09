import collections
import glob
import hashlib
import os
import random
import re
import shutil
import sys
import uuid

import requests
import  simplejson as json

import neolib.neoutil as neolib
import neolib.neoutil4Win as neolib4Win

class ChanageMp3Title(neolib.NeoRunnableClasss):
	maptitle = {'데려다줄래': '01', 'L.I.E': '02', '알면서': '03', 'HELLO(하니SOLO)': '04', 'CREAM': '05', '3%(솔지SOLO)': '06',
				'ONLYONE': '07', '당연해': '08', '냠냠쩝쩝(정화&혜린)': '09', '여름,가을,겨울,봄': '10', 'GOOD': '11',
				'HOTPINK(REMIX)': '12',
				'L.I.E(JANNABIMIX)': '13',}
	basepath = 'E:\\mp3\\EXID STREET'

	def doRun(self):


		for file in glob.glob(basepath + '\\*.mp3'):
			fname = os.path.basename(file)

			realname = re.sub(r"(.+)_EXID\(이엑스아이디\)_STREET\.mp3", r"\1", fname)

			strcmp = realname.replace(" ", "")
			strcmp = strcmp.upper()
			# print(strcmp in maptitle.keys())
			newfilename = "{0}\\{1}.{2}.mp3".format(basepath, self.maptitle[strcmp], realname)
			print(newfilename)
			shutil.move(file, newfilename)
			aaa = 34

class RunnableHexString(neolib.NeoRunnableClasss):
	def doRun(self):
		# result = bytearray.fromhex('deadbeef')
		byteform = neolib.HexString2Text(
			'02 30 34 31 37 30 39 32 30 36 30 49 30 4B 4B 1C 32 33 34 35 36 37 38 39 30 31 1C 30 33 36 37 1C 36 31 35 33 31 30 39 34 31 32 38 30 1C 30 30 31 1C 45 4E 30 37 23 23 23 53 4D 54 2D 44 33 35 30 43 31 31 30 31 23 23 23 23 53 4D 54 2D 54 32 32 34 31 30 30 31 30 30 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 30 31 34 30 41 6C 42 77 63 48 42 77 63 44 41 77 4D 44 41 78 55 45 32 46 46 46 41 41 41 41 49 41 41 41 42 41 71 6F 2B 50 31 4D 73 4C 5A 42 75 36 49 67 6D 78 35 6A 4A 32 44 36 5A 46 6D 64 76 46 35 63 62 58 7A 57 65 56 53 56 61 42 4D 35 68 32 32 65 6C 42 51 71 4A 68 47 69 54 4E 59 6E 51 68 79 2B 4F 38 33 50 4C 67 78 6F 64 35 51 4C 66 7A 52 4E 72 2F 30 64 6B 46 50 52 44 79 39 6B 69 6E 41 34 58 56 34 58 41 47 63 79 6D 56 67 2F 48 61 1C 1C 31 30 30 30 1C 1C 39 30 1C 31 36 30 36 30 31 1C 31 1C 30 31 1C 30 35 31 30 30 30 31 30 1C 31 30 32 30 33 30 34 30 35 30 36 30 37 30 38 30 38 30 31 34 30 36 30 36 30 31 30 33 41 30 41 38 30 32 41 41 42 42 43 43 44 44 30 32 38 32 30 30 30 30 30 30 38 38 30 30 31 36 30 36 30 31 30 30 37 43 30 30 31 45 30 33 30 30 20 20 36 30 32 38 43 30 32 32 41 30 31 31 30 30 30 31 30 30 30 30 31 36 41 30 30 30 30 30 30 30 32 35 30 31 30 34 30 32 30 30 30 31 30 33 36 36 30 35 31 30 1C 1C 1C 03 39 42 34 38',
			'utf-8')
		print(byteform)
		resttr = bytes.fromhex(
			'416C427763484277634441774D44417855453246464641414141494141414241716F2B50314D734C5A42753649676D78356A4A3244365A466D647646356362587A576556535661424D35683232656C4251714A684769544E596E5168792B4F3833504C67786F6435514C667A524E722F30646B4650524479396B696E413458563458414763796D56672F4861').decode(
			'utf-8')
		print(resttr)
		result = base64.standard_b64decode(resttr)
		hexstring = ''.join('{:02X} '.format(x) for x in result)
		print(result)
		print(hexstring)

class RunnableDrowDC(neolib.NeoRunnableClasss):
	def doRun(self):
		hdc = win32gui.GetDC(None, )
		cpen = win32gui.CreatePen(win32con.PS_COSMETIC, 10, win32api.RGB(255, 0, 0))
		coldpen = win32gui.SelectObject(hdc, cpen)

		win32gui.Rectangle(hdc, 100, 100, 300, 300)

		coldpen = win32gui.SelectObject(hdc, coldpen)
		win32gui.ReleaseDC(None, hdc)



class RunnableChangePath(neolib.NeoRunnableClasss):
	def doRun(self):
		path = "Z:\\Smartro\\산출물\\"

		print(path)
		fp = open(path + "out.txt", "w")
		for path, dirs, files in os.walk(path):
			for tmpfile in files:
				fullpath = "\\".join((path, tmpfile))
				print(tmpfile)
				fname, ext = os.path.splitext(fullpath)
				fp.write(tmpfile + "\t" + re.sub(r"\.", r"", ext) + "\n")
			break

		print(re.sub("a", "", "testaa"))
		print(neolib.listarg2Map(list))

		fp.close()



class Object:
	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
			sort_keys=True, indent=4)


class Protocol:
	def __init__(self):
		self.cmd = "TEST"
		self.value = {"aa":"bbb"}
		self.crc16 = "1818"

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
						  sort_keys=True, indent=4)

def object_decoder(obj):
	if '__type__' in obj and obj['__type__'] == 'Protocol':
		return Protocol(obj['name'], obj['username'])
	return obj

class TestSimpleClientRunnable(neolib.NeoRunnableClasss):
	def doRun(self):


		me = Object()
		me.name = "Onur"
		me.age = 35
		me.dog = Object()
		me.dog.name = "Apollo"

		print(me.to_JSON())

		proto = Protocol();

		print(proto.to_JSON())

		# create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# get local machine name
		# host = socket.gethostname()
		host = "218.159.79.99"

		port = 55510

		# connection to hostname on the port.
		s.connect((host, port))

		strbuff = proto.to_JSON()

		'{  "cmd": "START",   "crc16": "1818",            "value": { "": ""} }'


		buff = strbuff.encode()

		size = len(buff)
		print("buff {0} size:{1}".format(neolib.ByteArray2HexString(buff,''),size))
		s.send(size.to_bytes(4, byteorder='big'))

		s.send(buff);

		# Receive no more than 1024 bytes
		tm = s.recv(4)

		rsize = int.from_bytes(tm, 'big')
		print("r buff size:{0}".format(size))

		tm = s.recv(rsize)
		strrcev = tm.decode('utf-8')
		print("The time got from the server is %s" % strrcev)
		#rproto = json.loads(strrcev, object_hook=object_decoder)

	   # print(rproto)



		s.close()


class TestGiant2ClientRunnable(neolib.NeoRunnableClasss):
	sndjson = [
		{"cmd": "REQ_SESSION", "crc16": "", "mapvValue": {}},
		{"cmd": "REQ_CONFIRM", "crc16": "", "mapvValue": {"UID": "ssn_84", "SN": "012350AA53213799EE",
														  "MAC": "0025FAA2B506AFF1B59F47DEF02472316F3512742DD482863939FC9365450DC4"}},

		{"cmd": "REQ_POSITION", "mapvValue": {"UID": "ssn_84", "POSTYPE": "GPS", "POS_INFO": "서울특별시"}, "crc16": ""},
	]

	def SubHexStr(self, ORG, stindex,count):
		return ORG[stindex * 2: stindex * 2 + count* 2]

	def CalcMAC(self, key,  strChallenge,  SN):

		if len(SN) != 9 * 2:
			return


		sector0 = "0000A1AC57FF404E45D40401BD0ED3C673D3B7B82D85D9F313B55EDA3D940000"
				#'0000A1AC57FF404E45D40401BD0ED3C673D3B7B82D85D9F313B55EDA3D940000'

		SN01 = self.SubHexStr(SN,0,2) # [0 * 2: 0 * 2 + 2 * 2]   #; // "0123";
		SN23 = self.SubHexStr(SN,2,2) #SN[2 * 2: 2 * 2 + 2 * 2]   #; // "50AA";
		SN47 = self.SubHexStr(SN,4,4) #SN[2 * 4: 2 * 4 + 2 * 4]   #; // "53213799";
		SN8 = self.SubHexStr(SN,8,1) #SN[2 * 8: 2 * 4 + 2 * 1]  #; // "EE";

		Zero11 = "0000000000000000000000";
		shaInput = key + strChallenge + "08400000" + Zero11 + SN8 + SN47 + SN01 + SN23
		print("shaInput:\n"+shaInput)
		resbyte = hashlib.sha256(neolib.HexString2ByteArray(shaInput))
		hex_dig = resbyte.hexdigest()


		return hex_dig.upper()  # neolib.ByteArray2HexString(resbyte.hexdigest(),'').upper()

	def start(self):
		# create a socket object
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# get local machine name
		# host = socket.gethostname()
		host = "192.168.0.76"

		port = 5510

		# connection to hostname on the port.
		self.s.connect((host, port))



	def doUnit(self,strsnd):
		buff = strsnd.encode()

		size = len(buff)
		print("buff {0} size:{1}".format(neolib.ByteArray2HexString(buff, ''), size))
		self.s.send(size.to_bytes(4, byteorder='big'))

		self.s.send(buff);

		# Receive no more than 1024 bytes
		tm = self.s.recv(4)

		rsize = int.from_bytes(tm, 'big')
		print("r buff size:{0}".format(size))

		tm = self.s.recv(rsize)

		return tm.decode('utf-8')

	def doEnd(self):
		self.s.close()


	def doRun(self):

		self.start()



		for tmp in self.sndjson:
			map = tmp['mapvValue']
			if tmp["cmd"] == 'REQ_SESSION':

				None
			elif tmp["cmd"] == 'REQ_CONFIRM':
				map['UID'] = mapSession['UID']
				map['MAC'] = self.CalcMAC('0000A1AC57FF404E45D40401BD0ED3C673D3B7B82D85D9F313B55EDA3D940000',
									 mapValue['RN'],
									 '012350AA53213799EE'

									 )

				None

			elif tmp["cmd"] == 'REQ_POSITION':
				map['UID'] = mapSession['UID']

				None

			strsnd = json.dumps(tmp)

			strrcev = self.doUnit(strsnd)


			print("The time got from the server is %s" % strrcev)

			#rproto = json.loads(strrcev, object_hook=object_decoder)
			rproto = json.loads(strrcev)

			mapValue = rproto["mapvValue"]


			if tmp["cmd"] == 'REQ_SESSION':
				mapSession = mapValue






			print(rproto["mapvValue"])
			self.doEnd()












class TestHTTPCLient(TestGiant2ClientRunnable):
	def compress(self,str):
		s_out =gzip.compress(str.encode())
		sret = base64.b64encode(s_out).decode()

		print(sret)
		sret = sret.replace('+','-').replace( '/', '_')
		print(sret)



		print(base64.urlsafe_b64encode(s_out).decode())




		return base64.urlsafe_b64encode(s_out).decode()

	def decompress(self,str):
		print(str)

	   # str = str.replace('-', '+').replace('_', '/')
		#str += "="
		print(str)

		#s_out = base64.b64decode(str.encode())


		s_out =base64.urlsafe_b64decode(str.encode())
		return gzip.decompress(s_out).decode();

	def start(self):
		self.conn = http.client.HTTPConnection('localhost:8080')
		print(self.conn);

	def doUnit(self, strsnd):


		compjson =self.compress(strsnd)
		print(strsnd)
		print(compjson)
		strrequest = "/giant2Auth/NFC?cmd=CMDBYJSON&jsonbase64={0}".format(compjson)

		print(strrequest)

		self.conn.request("GET", strrequest)

		resp = self.conn.getresponse()
		print(resp.status, resp.reason)
		recvcompress = resp.read().decode()
		print(recvcompress)


		return self.decompress(recvcompress)

	def doEnd(self):
		self.conn.close()

	def doRun(self):

		conn = http.client.HTTPConnection('localhost:8080')
		print(conn);

		strjson = json.dumps({"mapvValue": {"UID": "ssn_307", "POSTYPE": "GPS", "POS_INFO": "테스트2"}, "crc16": "", "cmd": "REQ_POSITION"})

		print(strjson)

		strrequest = "/giant2Auth/NFC?cmd=CMDBYJSON_ROW&jsonbase64={0}".format('{"cmd":"REQ_POSITION","mapvValue":{"UID":"ssn_307","POSTYPE":"GPS","POS_INFO":""},"crc16":""}')

		print(strrequest)

		conn.request("GET",strrequest )
		resp = conn.getresponse()
		print(resp.status, resp.reason)
		data1 = resp.read()
		print(data1.decode())

		None




class RunnableHTTPCLient369(neolib.NeoRunnableClasss):
	url = 'https://www.annma.net/g5/bbs/board.php?bo_table=profile&wr_id=141'
	patt = r'<img\s+src="([a-zA-Z0-9/.:]+)"\s+alt="([a-zA-Z0-9]+)"\s*/>'
	kkjjiimg = "2m2szTIpIW";
	dayimg = "1RWbHAyiXm";
	nightimg = "1m9RfmwuNy";
	endimgnightimg = "kx0amYpu";

	def doRun(self):

		r = requests.get(self.url)
		results = re.findall(self.patt, r.text)

		fmt = '<img src="http://369am.diskn.com/%s" width = "300"/> <br />\n'

		for vars in results:
			print(fmt % vars[1])







		#print(r.text)




		None


class RunnablePHPCnovert(neolib.NeoRunnableClasss):


	def ReadString(self,orgpath):
		f = open(orgpath, 'rb')
		str = ''
		while True:
			buff = f.read(4096)
			unitstr = buff.decode('euc-kr')
			size = len(unitstr)

			if size == 0: break
			str += unitstr


		f.close()
		return  str

	def WriteString(self, dstpath,contents):
		file = open(dstpath, 'wb');
		file.write(contents.encode())
		file.close()

	def doRun(self):
		orgsrc = 'D:/PROJECT/ADVANCE/6765-E_approval/approval'
		dstdir = 'D:/PROJECT/ADVANCE/6765-E_approval/approval_new'

		for root, subdirs, files in os.walk(orgsrc):
			print('dir:'+root)
			dstpath = root.replace(orgsrc,dstdir)
			print('dstpath:' + dstpath)
			for filename in list(filter(lambda x: x.split(".")[-1] == 'php', files)):
				orgfile = os.path.join(root, filename)
				dstfile = os.path.join(dstpath, filename)
				self.ProcessChagneFiles(orgfile,dstfile)

			#for filename in files:
				print('\t'+os.path.join(root, filename))




		#self.ProcessChagneFiles(orgsrc,dstpath)


	def ProcessChagneFiles (self,orgpath,dstpath):

		#orgsrc ='D:/PROJECT/ADVANCE/6765-E_approval/approval/index.php'
		contents = self.ReadString(orgpath)

		newpath = os.path.dirname(dstpath)
		if not os.path.exists(newpath):
			os.makedirs(newpath)


		contents = re.sub(r'euc-kr', r'utf-8', contents)

		contents = re.sub(r'<\?\r\n',r'<?php\r\n',contents)

	  #  print(contents)
		self.WriteString(dstpath,contents)

class RunnableViewAsciiForm(neolib.NeoRunnableClasss):

	def Form2Byte(self,instr):
		print(instr)
		for tmp in instr.encode():
			print(tmp)
	def MakeMap(self):
		self.map = {}
		self.maprev = {}

		for item in range(ord('@'), ord('_') + 1):
			realvalue = item - 64
			ascii = "^" + chr(item)
			self.map[ascii] = realvalue
			self.maprev[realvalue] = ascii
			print("{0} {1}".format(ascii, hex(realvalue)))


	def doRun(self):
		self.MakeMap();

		fdsafs = sys.argv[1]
		#self.Form2Byte(fdsafs)
		None

class RunnableCompareMatch(neolib.NeoRunnableClasss):
	def doRun(self):


		str = neolib.StrFromFile('rsc/comp1.txt')
		str2 = neolib.StrFromFile('rsc/comp2.txt')
		arr =json.loads(str)
		arr2 = json.loads(str2)
		for tmp in arr:
			if tmp in arr2:
				arr2.remove(tmp)
				arr.remove(tmp)

		print(arr)
		print(arr2)


		None

class STC_A_605_04(neolib.NeoRunnableClasss):
	def test(self):
		None

class RunnableLogExtract(neolib.NeoRunnableClasss):
	def doRun(self):
		stgr = neolib.StrFromFile('rsc/log.txt')
		regpatt =  r'\n(02)([A-F0-9]{4})(51)([A-F0-9]{8})([A-F0-9]{4})([A-F0-9]*)(03)([A-F0-9]{2})'

		ret = re.findall(regpatt,stgr)
		strres = ''
		for  STX,PACKETLENGTH,FC,OFFSET,LENGTH,DATA,ETX,LRC in ret:
			offset = int.from_bytes(neolib.HexString2ByteArray(OFFSET), byteorder='big')
			length = int.from_bytes(neolib.HexString2ByteArray(LENGTH), byteorder='big')
			strres +='{0}\t{2}'.format(offset,OFFSET,length,LENGTH,offset+length)




class Runnable369Profile(neolib.NeoRunnableClasss):
	pattStartPrfofile = r'<img\s+src="http://369am.diskn.com/1RWbHAyiXm"\s+alt="1RWbHAyiXm"\s* />\s*<\s*br\s*/\s*>'
	pattEndPrfofile = r'<\s*/\s*div\s*>'
	pattProfile = r'<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />\s*([가-힣]+)(<img src="http://369am.diskn.com/[a-zA-Z0-9]+" alt="([a-zA-Z0-9]+)" />)*'

	def getProfileBlock(self,str):
		startIndex = 0
		endindex = 0;
		for match in re.finditer(self.pattStartPrfofile, str):
			startIndex = match.span()[1]
			print(match.span())

		str = str[startIndex:]
		match = re.search(self.pattEndPrfofile, str)

		endindex = match.span()[1]

		print(str[0:endindex])

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




	def doRun(self):
		str = neolib.StrFromFile('test/ref.html')
		str = self.getProfileBlock(str)
		print(str)

		mapProfile  = self.extractProfileMap(str)

		#
		# str  = str.replace("\r","");
		# str = str.replace("\n", "");
		#
		# list = re.split(r'<br\s*/\s*>',str)
		#
		# rearrstr = '\n'.join(list)
		#
		# mapProfile = {}
		# for tmp in re.findall(self.pattProfile,rearrstr):
		# 	extprofile = ''
		# 	if(len(tmp) == 4):
		# 		extprofile = tmp[3]
		# 	mapProfile[tmp[1]] = (tmp[0],extprofile)

		print(mapProfile)
class Test:
	def __init__(self):
		print('TEST')
		None
neolib.removeEmptyFolder("D:/내문서")
exit()
def deffilter(root,file):
	ext = neolib.getExtNameFromPath(file)
	if root in ['D:/내문서','D:/내문서/2015','D:/내문서/NEWDOC','D:/내문서/역량평가','D:/내문서/연말정산'] : return False
	if ext in ['.doc','.docx'] : return  True
	return  False
lista =	neolib.listAllFile("D:/내문서",deffilter)
for path in lista: print(path)
exit()
for root,file in lista:
	dstfile = "D:/내문서/NEWDOC/" + file
	newfile = file
	ext = neolib.getExtNameFromPath(file)
	while os.path.exists(dstfile):
		newfile = "COPY "+newfile
		dstfile = "D:/내문서/NEWDOC/" + newfile

	print("%s=>\n%s"%(root+"/"+file,dstfile))
	shutil.move(root+"/"+file,dstfile)

#print(lista)
exit()
#os.rmdir('D:/내문서/test')
#exit()
#shutil.rmtree('D:/내문서/test')
listaa = []
for root, dirs, files in os.walk("D:/내문서"):
	#print(root,len(files),len(dirs))
	sublen = len(files)+ len(dirs)
	if sublen == 0 : listaa.append(root)
	for basename in files:
		None
if len(listaa) == 0: exit()

for tmp in listaa:
	#shutil.rmtree(tmp)
	print(tmp)
	os.rmdir(tmp)



exit()
for tmp in range(0,10):
	print(str(uuid.uuid4()).upper())


exit()
test.sample.RunnableTmp().Run()
print(sys.path)
exit()





listMapOldDBMainProtocol = collections.OrderedDict([('aa1','bb1')])
listMapOldDBMainProtocol['aa'] ='bb'
listMapOldDBMainProtocol['a2'] ='bb'
listMapOldDBMainProtocol['a3'] ='bb'
print(listMapOldDBMainProtocol)


maprow = {"test":"vale","test1":"vale",}



arraycol = { tmp:maprow[tmp] for tmp in maprow}
print(maprow)
print(arraycol)

arraycol = collections.OrderedDict([('aa1','bb1') for key,value in maprow.items()])
print(arraycol)

arraycol = list(map(lambda tmp:tmp[0],maprow.items()))
#arraycol = list(map(lambda key:key.key,maprow))
print(arraycol)

exit()
Runnable369Profile().Run()
#TestLogExtract().Run()

#PuttyRunNMove.PuttyRunNMove().Run()

#TestDrowDC().Run();

exit()
url = 'http://bit.ly/2bB1LCD'
#url = 'https://www.doortodoor.co.kr'
r = requests.get(url)
print(r.text)
fb = open('out.txt','wb')
fb.write(r.text.encode())
fb.close()

exit()
maptest = {'test1':'111111','test2':'222222'}

for k,v in maptest.items():
	print(k,v)


exit()

RunnableCompareMatch().Run()
url = 'https://www.annma.net/g5/bbs/board.php?bo_table=profile&wr_id=141'
r = requests.get(url)
fb = open('out.txt','wb')
fb.write(r.text.encode())
fb.close()

exit()
RunnableViewAsciiForm().Run();





exit()

id = '409629'

safdasf = r'[{"name":"STX","length":1,"variable":false,"encodingOption":1,"strPacket":"02","calcLengthPython":null,"makePacketPython":null,"makeOrder":0},{"name":"LENGTH","length":4,"variable":false,"encodingOption":0,"strPacket":null,"calcLengthPython":null,"makePacketPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\MakeProtocolLength.py","makeOrder":-1},{"name":"DATA1","length":5,"variable":false,"encodingOption":0,"strPacket":"ABCDE","calcLengthPython":null,"makePacketPython":null,"makeOrder":0},{"name":"DATA2LENGTH","length":2,"variable":false,"encodingOption":1,"strPacket":null,"calcLengthPython":null,"makePacketPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\MakeDATALength.py","makeOrder":0},{"name":"DATA2","length":256,"variable":true,"encodingOption":1,"strPacket":"165704","calcLengthPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\CalcDATALength.py","makePacketPython":null,"makeOrder":0},{"name":"DATA3LENGTH","length":2,"variable":false,"encodingOption":1,"strPacket":null,"calcLengthPython":null,"makePacketPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\MakeDATALength.py","makeOrder":0},{"name":"DATA3","length":256,"variable":true,"encodingOption":2,"strPacket":"AAED","calcLengthPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\CalcDATALength.py","makePacketPython":null,"makeOrder":0},{"name":"CRC","length":2,"variable":false,"encodingOption":1,"strPacket":null,"calcLengthPython":null,"makePacketPython":"D:\\PROJECT\\자동단말기검수\\SRC\\Protocol_Parser\\WindowsFormsApplication1\\bin\\x86\\Debug\\scripts\\MakeProtocolCRC.py","makeOrder":0},{"name":"ETX","length":1,"variable":false,"encodingOption":1,"strPacket":"03","calcLengthPython":null,"makePacketPython":null,"makeOrder":0}]'

print(safdasf)
sdaf = json.loads(safdasf);

print(sdaf)
fsdafasf  =json.dumps(sdaf)
print(fsdafasf)

exit()

#nicklist = requests.get("http://localhost/PWDSERVER/webtoon.php?option=todaylist")
nicklist = requests.get("http://neo1seok.iptime.org/PWDSERVER/webtoon.php?option=todaylist")
print(nicklist.text.encode())
exit()
startstgtr = '<td class="title">'
index = nicklist.text.index(startstgtr)
str = nicklist.text[index:]
regexp = r"/webtoon/detail.nhn\?titleId="+id+r"&no=(\d{1,4}).*"
results = re.search(regexp, str)
print(results.group(1))

str = '["foo", {"bar":["baz", null, 1.0, 2]}]'

safdsf = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
fsdf = json.loads(safdsf )

array = ['시작일시 입력','종료일시 입력','삭제','직불','현금','부가기능','봉사료율 설정','취소-일반영수증','취소-자진발급','취소-직불거래','추가환경설정','Condition 입력','사인패드입력','Send ENQ','초기키주입전문송신','초기키주입전문수신','조회-유가보조금조회','취소-보너스적립','정산-거래일자별집계','ReCheckData']
safdfwsfdf = json.dumps(array)


exit()

array = ['시작일시 입력','종료일시 입력','삭제','직불','현금','부가기능','봉사료율 설정','취소-일반영수증','취소-자진발급','취소-직불거래','추가환경설정','Condition 입력','사인패드입력','Send ENQ','초기키주입전문송신','초기키주입전문수신','조회-유가보조금조회','취소-보너스적립','정산-거래일자별집계','ReCheckData']

str = neolib4Win.GetClipBoard()

strarray = str.split("\n")
strarray = ['거래금액 입력','할부개월 입력','부가세 입력','봉사료 입력','승인번호 입력','카드번호 입력','유효기간 입력','거래일련번호 입력','매출일자 입력','수표번호 입력','발행일자 입력','비밀번호 입력','계좌번호 입력','주민등록번호 입력','사업자번호 입력','취소금액 입력','지역번호 입력','전화번호 입력','시작일시 입력','종료일시 입력','숫자+입력','숫자','0','000','특수','삭제','종료','입력','조회','정산','재인쇄','직불','현금','포인트','부가기능','HWTrace','STMS개시거래','가맹점정보확인','개시거래','거래일련번호','메모리초기화','면세유','봉사료율 설정','부가세율 설정','상품다운로드','설정-기타품목사용','수표조회-가계수표','수표조회-당좌수표','수표조회-자기앞수표','은련','전화등록','정산-거래내역삭제','정산-거래별일시집계','정산-교대마감','정산-교대마감재인쇄','정산-내역인쇄','정산방식변경','정산-일마감','조회-단말기실적검색','조회-보너스','직불-거래확인','직불-승인','직불-잔액조회','직불-취소','취소-사업자지출증빙','취소-소비자소득공제','취소-신용거래','취소-원천징수','취소-일반영수증','취소-자진발급','취소-직불거래','취소-직전거래','키인승인-신용거래승인','키인승인-신용거래취소','통신STMS설정','통신접속설정','통신테스트','포인트','현금IC-거래조회','현금IC-승인','현금IC-잔액조회','현금IC-취소','현금-사업자지출증빙','현금-소비자소득공제','현금-원천징수','현금-일반영수증','현금-자진발급','조회-유가보조금조회','취소-모바일쿠폰','취소-보너스적립','신용카드','수표조회','화물차-일반승인','화물차-거래카드승인','화물차-거래체크카드','모바일쿠폰-신용카드결제','모바일쿠폰-현금영수증결제','모바일쿠폰-쿠폰단독결제','노즐거래','노즐신용','정산-거래일자별집계','정산-거래일시별집계','설정-정보보안기능','KeyExchange','FirstKeyMergy','CheckData','ReCheckData','설정-시간설정','설정-POS','설정-기타서비스','설정-유종설정','Message','추가환경설정','MS Swipe','Smart Card Insert','Smart Card Eject','Condition 입력','요청 전문 수신','응답 전문 송신','Image','PORT 끊기','PORT 복구','설정 초기화','통신 선택','Profile 선택','사인패드입력','PINPAD 입력','수표조회기 입력','접속연결','FOR','NEXT','Send ENQ','Test KeyPAD','Test MS','Test Smart Card','초기키주입전문송신','초기키주입전문수신','POS 요청 전문 송신','POS 응답 전문 수신','Dongle 요청 전문 송신','Dongle 응답 전문 수신']
newstrarray = []

for tmp in strarray:
	if tmp == 'Condition 입력':
		adf = 34

	if tmp in array:
		tmp += '-->삭제'
	newstrarray.append(tmp)

for tmp in newstrarray:
	print(tmp)


neolib4Win.SetClipBoard('\n'.join(newstrarray))



exit()
RunnablePHPCnovert().Run()

print(sys.stdin.encoding)



exit()


RunnableHTTPCLient369().Run();


x = [random.choice('0123456789ABCDEF') for p in range(0, 64)]

salt = "".join(x)

salt = "76EC5DC96D31DF9F98BB5E322BD682B459F49B73A2625D47900CC59172ED2E9F"
print("SALT:\n{0}".format(salt))


resbyte = hashlib.sha256(("tofhdna1pwd"+salt).encode())
hex_dig = resbyte.hexdigest()

print(hex_dig.upper())



#TestDisplay().doRun()

#TestSimpleClientTest().doRun()
#TestGiant2ClientTest().doRun()
#TestHTTPCLient().doRun()


#print(neolib.Text2HexString("pPpp", 'utf-8', ' '))


exit()

exit()


exit();


exit()


exit()

basepath = 'D:\\PROJECT\\스마트로\\TEMP\\SMARTRO_new3\\SMARTRO\\bin'

fp = open("D:\\PROJECT\\스마트로\\TEMP\\SMARTRO_new3\\SMARTRO\\bin\\out.txt", "w")
for file in glob.glob(basepath + '\\*.*'):
	fp.write(os.path.basename(file) + "\n")

files = list(map(lambda x: os.path.basename(x), glob.glob(basepath + '\\*.*')))
mapfiles = dict((os.path.basename(v), v) for v in glob.glob(basepath + '\\*.*'))

print("FILES:")
print(mapfiles)

fp.close()

print(sys.argv)

exit()

