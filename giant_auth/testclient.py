import socket
import neolib.neolib as neolib
import time
import threading

class TestClient(neolib.NeoRunnableClasss):
	def __init__(self):
		#self.hostport = ('203.187.186.136', 40410)
		#self.hostport = ('localhost', 5510)
		#self.hostport = ('192.168.0.77', 5510)
		self.hostport = ('dev.ictk.com', 5510)
		self.threads = {}

		None
	def parseFromBuff(self,buff):
		print(neolib.ByteArray2HexString(buff))
		lrc = self.LRC(buff, 0, len(buff) - 1)
		print(lrc)

		stx = buff[0:1]
		blength = buff[1:3]
		size = int.from_bytes(blength, byteorder='big')

		print(size)
		cmd = buff[3:4]
		icmd = int.from_bytes(cmd, byteorder='big')
		data = buff[4:4 + size]
		etx = buff[4 + size:4 + size + 1]
		lrc = buff[4 + size + 1:4 + size + 2]
		return stx, size, icmd, data, etx, lrc

	def LRC(self, buff, st, ed):
		res = 0;
		for tmp in buff[st:ed]:
			res = res ^ tmp
		return res.to_bytes(1, byteorder='big')

	def maketoBuff(self,icmd, data):
		resbuff = b"\x02"
		resbuff += (len(data)+1).to_bytes(2, byteorder='big')
		resbuff += icmd.to_bytes(1, byteorder='big')
		resbuff += data
		resbuff += b"\x03"
		resbuff += self.LRC(resbuff, 1, len(resbuff))

		return resbuff
	def proClient(self,buff):
		print(neolib.ByteArray2HexString(buff))
		stx = buff[0:1]
		blength = buff[1:3]
		size = int.from_bytes(blength,byteorder='big')
		print(size)
		cmd = buff[3:4]
		print(stx,blength,cmd)

		return
	def procReqServ(self,s,icmd,hexstrdat):
		buff = self.maketoBuff(icmd,	  neolib.HexString2ByteArray(hexstrdat))
		print(threading.current_thread(),"snd",neolib.ByteArray2HexString(buff))
		s.send(buff)
		rbuff = s.recv(1024)
		res = self.parseFromBuff(rbuff)
		print(threading.current_thread(),"rcv",neolib.ByteArray2HexString(rbuff))
		print(threading.current_thread(),"res", res)





	def procSerrv(self,hostport):
		host = hostport[0]
		port = hostport[1]
		# create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



		# connection to hostname on the port.
		s.connect((host, port))

		#s.send('test'.encode())
		# Receive no more than 1024 bytes

		self.procReqServ(0x10,"4C4715000000000047")
#procReqServ(0x10,"4C4722334455667747")
		time.sleep(0.1)


		self.procReqServ(0x11,"14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")
# procReqServ(0x12,"")
# procReqServ(0x13,"14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")
# procReqServ(0x14,"01")
#procReqServ(0x15,"EF3540954ED55F6F10C5173CB6EC27E5")
		self.procReqServ(s,0x10,"4C4715000000000047")
		#procReqServ(0x10,"4C4722334455667747")
		#time.sleep(10)

		self.procReqServ(s,0x11,"14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")
		self.procReqServ(s,0x12,"")
		self.procReqServ(s,0x13,"14A148EF48A7863A930BEF984C6411E3EF3540954ED55F6F10C5173CB6EC27E5")
		self.procReqServ(s,0x14,"01")
		self.procReqServ(s,0x15,"EF3540954ED55F6F10C5173CB6EC27E5")



		s.close()
	def worker(self):
		self.procSerrv(self.hostport)
		None
	def doRun(self):
		for idx in range(1):
			t = threading.Thread(target=self.worker)
			self.threads[idx] = t
			t.start()

		while 1:
			time.sleep(1)
			None

		None


#hostport = ('localhost',5510)

# hostport = ('203.187.186.136',40410)
# procSerrv(hostport)
#print("The time got from the server is %s" % tm.decode('ascii'))
TestClient().Run()