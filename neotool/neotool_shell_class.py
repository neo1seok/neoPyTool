import re
import sys
import win32api
import shutil
import neolib.neoutil as neolib
import neolib.neoutil4Win as neolib4Win
import win32ui
import win32con

def GetFileNameOrg(str):
	return str

def GetFileNameByQutoType(str):
	return re.sub(r'\\',r'\\\\\\',str)


class SetClipBoardPath(neolib.NeoRunnableClasss):
	mapfunction = {"literal": lambda x: re.sub(r'\\', r'\\\\', x),
				   "linux": lambda x: re.sub(r'\\', r'/', x),
				   "org": lambda x: x,
				   }
	def doRun(self):
		try:

			value = self.mapArgs["path"]
		except:
			value = ""

		try:
			pffile = self.mapfunction[self.mapArgs["type"]]
		except:
			pffile = self.mapfunction["org"]

		dststr = pffile(value)

		win32api.MessageBox(0, dststr, "NEOPYTHONSHELL")
		neolib4Win.SetClipBoard(dststr)

		None


class BaseMoveTo(neolib.NeoRunnableClasss):
	def InitRun(self):
		self.src_path = self.mapArgs["path"]

		None
	def doRun(self):
		msg = "{0}->{1}".format(self.src_path, self.dst_path)


		if win32ui.MessageBox(msg, "NEOPYTHONSHELL", win32con.MB_YESNOCANCEL) != win32con.IDYES:
			return

		shutil.move(self.src_path, self.dst_path)

		None

class MoveToBest(BaseMoveTo):
	dst_path = 'D:/down/zave/BEST'


class MoveToGood(BaseMoveTo):
	dst_path = 'D:/down/zave/good'
