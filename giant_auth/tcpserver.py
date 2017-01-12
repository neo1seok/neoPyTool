
import time
import neolib.neolib as neolib
import http
import  simplejson as json
import socket
import http.client
import requests
import logging
from logging import handlers

# create a socket object
class HandleClient:
	def __init__(self):
		self.mapProc = {
			0x10: (self.ReqStartSession, "REQ_START_SESSION"),
			0x11: (self.Authentication, "AUTHENTICATION"),
			0x12: (self.ReqHostchallenge, "REQ_HOSTCHALLENGE"),
			0x13: (self.ReqUpdateinfo, "REQ_UPDATEINFO"),
			0x14: (self.NotyUpdateresult, "NOTY_UPDATERESULT"),
			0x15: (self.ReqTransferData, "REQ_TRANSFER_DATA")

		}

		self.mapErro={
			"NO_SN": 0xf0,
			"NOT_MATCH_MAC": 0xf1,
			"NO_MASTERKEY": 0xf2,

		}
		#conn = http.client.HTTPConnection('localhost:8080')
		self.handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
		self.logger = self.createLogger("tcp_giant_auth", self.handler)
		self.logger.debug("%s __init__", self.__class__.__name__)

		self.conn = http.client.HTTPConnection('localhost:8080')

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

	def reqGet(self,mapvValue):
		jsonbase = json.dumps({"cmd": self.cmdname, "mapvValue": mapvValue})
		strrequest = "/giant_auth/auth?cmd=CMDBYJSON_ROW&type=debug&jsonbase64={0}".format(jsonbase)
		strrequest = strrequest.replace(" ","")
		print(strrequest)
		self.logger.debug("strrequest:%s", strrequest)
		self.conn.request("GET", strrequest)
		resp = self.conn.getresponse()

		#print(resp.status, resp.reason)
		self.logger.debug("%s", "{0} {1}".format(resp.status, resp.reason))
		data1 = resp.read()
		print(data1.decode())
		self.logger.debug("res:%s", data1.decode())
		res = json.loads(data1.decode());
		return res['mapvValue']

	def LRC(self,buff,st,ed):
		res = 0;
		for tmp in buff[st:ed]:
			res = res^tmp
		return res.to_bytes(1,byteorder='big')

	def maketoBuff(self,icmd,data):
		resbuff = b"\x02"
		resbuff += len(data).to_bytes(2,byteorder='big')
		resbuff += icmd.to_bytes(1, byteorder='big')
		resbuff += data
		resbuff += b"\x03"
		resbuff += self.LRC(resbuff,1,len(resbuff))

		return resbuff


	def parseFromBuff(self,buff):
		print(neolib.ByteArray2HexString(buff))
		lrc =  self.LRC(buff, 0, len(buff)-1)
		print(lrc)

		stx = buff[0:1]
		blength = buff[1:3]
		size = int.from_bytes(blength,byteorder='big')

		print(size)
		cmd = buff[3:4]
		icmd = int.from_bytes(cmd, byteorder='big')
		data = buff[4:4+size]
		etx = buff[4 + size:4 + size+1]
		lrc = buff[4 + size+1:4 + size+2]
		self.logger.debug("%s", "{0},{1},{2},{3},".format(stx,icmd,etx,lrc))
		self.logger.debug("DATA:%s",neolib.ByteArray2HexString(data))
		return 	stx,size,icmd,data,etx,lrc

	def processResult(self,mapSrv):
		result = mapSrv['result']
		error = mapSrv['error']
		if result == 'OK':
			return b'0x0';

		if error in self.mapErro:
			err = self.mapErro[error]
		else:
			err =0xff

		return  err.to_bytes(1, byteorder='big')





	def ReqStartSession(self,data):
		self.logger.debug("ReqStartSession")
		sn = data[0:9]

		self.mapSrv = self.reqGet({"sn": neolib.ByteArray2HexString(sn)})
		self.uid = self.mapSrv['uid']
		bchallenge = neolib.HexString2ByteArray(self.mapSrv['challenge'])
		return bchallenge

	def Authentication(self,data):
		self.logger.debug('Authentication')

		mac = data[0:32]
		self.mapSrv = self.reqGet({"uid":self.uid,"mac": neolib.ByteArray2HexString(mac)})
		bupdate = b'0x00'

		if self.mapSrv["result"] == "OK" and self.mapSrv['update'] == 'OK':
			bupdate = b'0x01'


		return bupdate
	def ReqHostchallenge(self,data):
		self.logger.debug('ReqHostchallenge')
		self.mapSrv = self.reqGet({"uid":self.uid})

		bhostchallenge = neolib.HexString2ByteArray(self.mapSrv['hostchallenge'])

		return bhostchallenge

	def ReqUpdateinfo(self,data):
		self.logger.debug('ReqUpdateinfo')
		gen_nonce = data[0:32]
		self.mapSrv = self.reqGet({"uid":self.uid,"gen_nonce": neolib.ByteArray2HexString(gen_nonce)})

		bwrite_code = neolib.HexString2ByteArray(self.mapSrv['write_code'])
		bmac = neolib.HexString2ByteArray(self.mapSrv['mac_write'])

		return bwrite_code+bmac
	def NotyUpdateresult(self,data):
		self.logger.debug('NotyUpdateresult')
		result = data[0:1]

		self.mapSrv = self.reqGet({"uid":self.uid,"result": neolib.ByteArray2HexString(result)})

		return b''
	def ReqTransferData(self,data):
		self.logger.debug('ReqTransferData')
		appid = data[0:16]
		self.mapSrv = self.reqGet({"uid":self.uid,"appid": neolib.ByteArray2HexString(appid)})

		bdata = neolib.HexString2ByteArray(self.mapSrv['data'])

		return bdata
	def doProc(self,buff):
		bresult = b'00'
		stx, size, icmd, data, etx, lrc = self.parseFromBuff(buff)
		processer = self.mapProc[icmd][0]
		self.cmdname = self.mapProc[icmd][1]
		resdata = b''
		try:
			resdata = processer(data)
		except Exception as ext:
			self.logger.error("%s",ext)

		self.bresult = self.processResult(self.mapSrv)


		return self.maketoBuff(icmd,bresult+resdata)

	def Test(self):


		dres = self.doProc(self.maketoBuff(0x10,neolib.HexString2ByteArray("4C472233445566774a")))
		dres = self.doProc(self.maketoBuff(0x11,neolib.HexString2ByteArray("14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")))
		dres = self.doProc(self.maketoBuff(0x12,b''))
		dres = self.doProc(self.maketoBuff(0x13,neolib.HexString2ByteArray("14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")))
		dres = self.doProc(self.maketoBuff(0x14,neolib.HexString2ByteArray("01")))
		dres = self.doProc(self.maketoBuff(0x15,neolib.HexString2ByteArray("EF3540954ED55F6F10C5173CB6EC27E5")))

	def RunServer(self):
		serversocket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM)

		# get local machine name
		host = '0.0.0.0'

		port = 5510

		# bind to the port
		serversocket.bind((host, port))

		# queue up to 5 requests
		serversocket.listen(5)

		while True:
			# establish a connection
			self.logger.debug('waiting')
			clientsocket, addr = serversocket.accept()
			handle = HandleClient()
			self.logger.debug("Got a connection from %s" % str(addr))
			while True:
				try:
					buff = clientsocket.recv(1024)
					self.logger.debug(buff)

					if buff == b'':
						break

					sndbuff = handle.doProc(buff)

					self.logger.debug(sndbuff)

					time.sleep(0.1)
					clientsocket.send(sndbuff)
					time.sleep(0.1)
				except Exception as ext:
					self.logger.debug(ext)
					break
			clientsocket.close()



#HandleClient().Test()
HandleClient().RunServer()
exit()

