import socket
import time

# create a socket object
serversocket = socket.socket(
			socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = '0.0.0.0'

port = 5511

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
	# establish a connection
	print('waiting')
	clientsocket,addr = serversocket.accept()
	print("Got a connection from %s" % str(addr))
	while True:
		try:
			buff = clientsocket.recv(128)
			print(buff)
			if buff == b'':
				break

			time.sleep(0.1)
			clientsocket.send(buff)
			time.sleep(0.1)
		except Exception as ext:
			print(ext)
			break
	clientsocket.close()