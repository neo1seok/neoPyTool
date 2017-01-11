import socket
import neolib.neolib as neolib


def proClient(buff):
	print(neolib.ByteArray2HexString(buff))
	stx = buff[0:1]
	blength = buff[1:3]
	size = int.from_bytes(blength,byteorder='big')
	print(size)
	cmd = buff[3:4]
	print(stx,blength,cmd)

	return
buff = neolib.HexString2ByteArray("020004100000000300")

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
host = 'localhost'
#host = "35.163.249.213"

port = 5510
#port = 51717

# connection to hostname on the port.
s.connect((host, port))

#s.send('test'.encode())
# Receive no more than 1024 bytes


size = len(buff)
s.send(buff)
tm = s.recv(128)
print(tm)
s.close()

print("The time got from the server is %s" % tm.decode('ascii'))