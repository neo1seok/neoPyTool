

import win32clipboard
import  re


class NeoTestClasss:
	def __init__(self):
		None

	def Run(self):
		self.InitRun()
		self.doRun()
		self.endRun()

	def InitRun(self):
		None

	def doRun(self):
		None

	def endRun(self):
		exit()



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

def ByteArray2HexString(bytes,sep) :
   return  sep.join('{:02X} '.format(x) for x in bytes)

def HexString2Text(hexstr,enc) :
    return HexString2ByteArray(hexstr).decode(enc)

def Text2HexString(str,enc,sep) :
    return ByteArray2HexString(str.encode(enc),sep)


