import socket
import neolib.neolib as neolib
import time
import hashlib
def substr(str,index,length):
	return str[index:index + length]
def SHA256(shaInput):
	m = hashlib.sha256()
	m.update(neolib.HexString2ByteArray(shaInput))
	reshash = m.digest()

	return neolib.ByteArray2HexString(reshash)

def verifyMAC(MAC, Challenge, SN):

	Sector1 = "1111111111111111111111111111111111111111111111111111111111111111"
	INS_Code = "08"
	P1 = "40"
	P2 = "0100"
	Zero_11 = "0000000000000000000000"

	shaInput = Sector1 + Challenge + INS_Code + P1 + P2 + Zero_11 + SN[16:16+ 2] + SN[8:8+ 8] + SN[0: 4] + SN[4:4+ 4]

	shaOut = SHA256(shaInput)


	if MAC==shaOut:
		return True
	else:
		return False


def XOR(strInput1,strInput2):


	if len(strInput1) != len(strInput2):
		return "";

	bInput1 = neolib.HexString2ByteArray(strInput1)
	bInput2 = neolib.HexString2ByteArray(strInput2)

	bLen = len(bInput1)

	bOutput = []

	for i in range(0,bLen):
		bOutput.append( bInput1[i] ^ bInput2[i])

	return  neolib.ByteArray2HexString(bOutput)



def	decrypt(	IV,	Cipher,	SN):

	Plain = "";

	Sector0 = "0000000000000000000000000000000000000000000000000000000000000000";
	INS_Code = "08";
	P1 = "00";
	P2 = "0000";
	Zero_24 = "000000000000000000000000000000000000000000000000";
	Challenge = IV + Zero_24;
	Zero_11 = "0000000000000000000000";
	SN_8 = SN[16:16+ 2]
	
	Zero_4 = "00000000";
	
	SN_01 = substr(SN,0, 4)
	
	Zero_2 = "0000";

	
	shaInput = Sector0 + Challenge + INS_Code + P1 + P2 + Zero_11 + SN_8 + Zero_4 + SN_01 + Zero_2;
	
	shaOut = SHA256(shaInput)

	PlainHex = XOR( shaOut, Cipher);

	return PlainHex;

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
host = "192.168.0.103"

#port = 5510
port = 51717

# connection to hostname on the port.
s.connect((host, port))

s.send('2'.encode())
# Receive no more than 1024 bytes
time.sleep(0.3)

SN = neolib.ByteArray2HexString(s.recv(1024))
time.sleep(0.3)
SN = SN[2:2+8] + SN[18: 18+10]

print(SN)

while True:
	s.send('1'.encode())
	recv = s.recv(1024)
	hex = neolib.ByteArray2HexString(recv)
	#print(hex)
	#print(str(recv[0]),str(recv[2]))

	IV = hex[8:8+ 16]
	Cipher = hex[24:24+ 64]
	MAC = hex[88: 88+64]
	#print(IV,Cipher,MAC)


	if verifyMAC(MAC, Cipher, SN):
	
		Plain = decrypt(substr(hex,8, 16), substr(hex,24, 64), SN);
		txtplain = substr(Plain,0, 8)
		hum = substr(Plain,0, 2)
		temp = substr(Plain, 4, 2)
		print(txtplain,hum,temp)


	else:
		print('INVALID')

	time.sleep(3)

s.close()

#print("The time got from the server is %s" % tm.decode('ascii'))