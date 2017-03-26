from  neolib.neoserver import *



class RemoteHandleClient(baseHandleClient):
	def	init(self):
		None
	def run(self):
		try:
			buff = self.clientsocket.recv(128)
			print(buff)
			if buff == b'':
				return

			time.sleep(0.1)
			self.clientsocket.send(buff)
			time.sleep(0.1)
		except Exception as ext:
			print(ext)
			return