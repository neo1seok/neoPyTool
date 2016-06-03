import sys
import neolib
import win32api
import time
import os
import datetime


class BaseRunClass:
	class_name = ""
	desc = ""
	objects = {}

	def __init__(self, maparg):
		self.maparg = maparg
		self.InitValue()


	def doRun(self):
		print('a')

	def InitValue(self):
		None


class SetClipBoard(BaseRunClass):
	mapstr = {"greeting": "안녕하십니까? ICTK 신원석입니다.\r\n오늘도 좋은 하루 되십시오.\r\n감사합니다.",
			  "deftype": "// 신원석(neo1seok) {0:%Y-%m-%d} : ".format(datetime.datetime.now())}

	def doRun(self):
		#	win32api.MessageBox(0, dststr, "NEOPYTHONSHELL")
		print("set clipboard:\n" + self.dststr)
		neolib.SetClipBoard(self.dststr)

	def InitValue(self):
		key = self.maparg['key']
		self.dststr = self.mapstr[key]


class classGreeting(SetClipBoard):
	dststr = "안녕하십니까? ICTK 신원석입니다.\r\n오늘도 좋은 하루 되십시오.\r\n감사합니다."


class classGenDefType(SetClipBoard):
	dststr = "// 신원석(neo1seok) {0:%Y-%m-%d} : ".format(datetime.datetime.now())


if __name__ != '__main__':
	exit()

maparg = neolib.listarg2Map(sys.argv)
mapfunction = {"strcpy": SetClipBoard(maparg)}

cmd = maparg["rt"]
print(maparg)
mapfunction[cmd]
mapfunction[cmd].doRun()
i = 5
while i > 0:
	time.sleep(1)  # delays for 5 seconds
	print(str(i) + "second left")
	i -= 1
