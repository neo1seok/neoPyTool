import socket
import neolib.neoutil as neolib


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
host = "192.168.0.76"

port = 5510

# connection to hostname on the port.
s.connect((host, port))


s.send(neolib.HexString2ByteArray('0000005E02307070707070303030303165101CAFF3EF6287000000350C000000303525537D752886C31BB5C32AB509B00FC068AE09B192B0C2AF349F11534BD4DAE55C4A423865B8E40E0259BA45DD27C810B323DB653DFC50F9E0A65ED6085CF670'))
# Receive no more than 1024 bytes
buff = s.recv(4)
rvsize = int.from_bytes(buff, byteorder='big', signed=False)
num = int(buff, 16)
buff = s.recv(rvsize)

print(neolib.ByteArray2HexString(buff))


s.close()
