

import win32clipboard
import  re
import subprocess

class NeoRunnableClasss:
	def __init__(self):
		None

	def Run(self):
		self.InitRun()
		#try:
		self.doRun()

		#except Exception as inst:
		#	print(inst.args)
		#finally:
		self.endRun()



	def InitRun(self):
		None

	def doRun(self):
		None

	def endRun(self):
		exit()


def executeAsync( cmd):
	fd = subprocess.Popen(cmd, shell=True,
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE,
						  stderr=subprocess.PIPE)
	return fd.stdout, fd.stderr

def listarg2Map(list):
	maparg = {}
	i = 0
	while i < len(list):
		value = list[i]


		if value.startswith("-"):
			value = re.sub("-","",value)
			print(value)
			nextvalue = list[i + 1] if i +1 < len(list) else ""
			nextvalue = "" if  nextvalue.startswith("-") else nextvalue

			maparg[value] = nextvalue


		i=i+1
	return maparg

def GetClipBoard():
	try:
		win32clipboard.OpenClipboard()
		strret = win32clipboard.GetClipboardData( win32clipboard.CF_UNICODETEXT)  # set clipboard data
		win32clipboard.CloseClipboard()

	except TypeError:
		pass

	return strret

def SetClipBoard(str):
	try:
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData( win32clipboard.CF_UNICODETEXT,str)  # set clipboard data
		win32clipboard.CloseClipboard()
	except TypeError:
		pass

def HexString2ByteArray(hexstr) :
	return bytes.fromhex(hexstr)

def ByteArray2HexString(bytes,sep="") :
   return  sep.join('{:02X}'.format(x) for x in bytes)

def HexString2Text(hexstr,enc="utf-8") :
	return HexString2ByteArray(hexstr).decode(enc)

def Text2HexString(str,enc="utf-8",sep="") :
	return ByteArray2HexString(str.encode(enc),sep)



def StrFromFile(filepath,enc='utf-8'):
	fb = open(filepath,'rb')
	rt = fb.read()
	str = rt.decode(enc)
	fb.close()
	return str

def StrToFile(str,filepath,enc='utf-8'):
	fb = open(filepath,'wb')
	fb.write(str.encode(enc))
	fb.close()
