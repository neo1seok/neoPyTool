import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
host = "192.168.0.76"

port = 5510

# connection to hostname on the port.
s.connect((host, port))

s.send()
# Receive no more than 1024 bytes
tm = s.recv(1024)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))