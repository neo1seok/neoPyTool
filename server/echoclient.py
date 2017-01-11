import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
#host = 'localhost'
host = "35.163.249.213"

port = 5511
#port = 51717

# connection to hostname on the port.
s.connect((host, port))

#s.send('test'.encode())
# Receive no more than 1024 bytes
buff = "1"*128
size = len(buff)
s.send(buff.encode())
tm = s.recv(128)
print(tm)
s.close()

print("The time got from the server is %s" % tm.decode('ascii'))