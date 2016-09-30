import re
import win32gui
import time
import datetime
import neolib
import sys
import win32api
import neolib4Win


class BaseRunClass(neolib.NeoRunnableClasss):
	class_name = ""
	desc = ""
	objects = {}

	def __init__(self, maparg):
		self.maparg = maparg
		self.InitValue()

	def InitValue(self):
		None
	#
	# def doRun(self):
	# 	print('a')
	#
	# def InitValue(self):
	# 	None


class SetClipBoard(BaseRunClass):
	mapstr = {"greeting": "안녕하십니까? ICTK 신원석입니다.\r\n\r\n\r\n오늘도 좋은 하루 되십시오.\r\n감사합니다.",
			  "greeting2": "툴RND팀 신원석입니다.\r\n\r\n\r\n수고하십시오.",
			  "deftype": "// 신원석(neo1seok) {0:%Y-%m-%d} : ".format(datetime.datetime.now())}

	def doRun(self):
		#	win32api.MessageBox(0, dststr, "NEOPYTHONSHELL")
		print("set clipboard:\n" + self.dststr)
		neolib4Win.SetClipBoard(self.dststr)

	def InitValue(self):
		try:
			key	= self.maparg['key']
		except:
			key = "greeting"



		self.dststr = self.mapstr[key]


class classGreeting(SetClipBoard):
	dststr = "안녕하십니까? ICTK 신원석입니다.\r\n오늘도 좋은 하루 되십시오.\r\n감사합니다."


class classGenDefType(SetClipBoard):
	dststr = "// 신원석(neo1seok) {0:%Y-%m-%d} : ".format(datetime.datetime.now())


class ConvertBaseClipboard(BaseRunClass):

	def convContents(self):
		None
	def doRun(self):
		self.dststr = neolib4Win.GetClipBoard()
		print("get clipboard:\n" + self.dststr,"\n")
		self.convContents()
		print("set clipboard:\n" , self.dststr,"\n")
		neolib4Win.SetClipBoard(self.dststr)


class ConvertMapCs2Java(ConvertBaseClipboard):
	def convContents(self):
		#print("get clipboard:\n" + self.dststr)
		realname = "TEST"
		realname = re.sub(r"\[(.+)\]", r".get(\1)", self.dststr)
		self.dststr = realname
		#print("set clipboard:\n" + self.dststr)
		None
"""
	def doRun(self):
		#	win32api.MessageBox(0, dststr, "NEOPYTHONSHELL")

		self.dststr = neolib.GetClipBoard()



		neolib.SetClipBoard(realname)
"""

class MakeNormalTxtInClipBoard(ConvertBaseClipboard):

	def convContents(self):
		#print("get clipboard:\n" + self.dststr)
		None
"""
	def doRun(self):
		self.dststr = neolib.GetClipBoard()
		print("get clipboard:\n" + self.dststr)
		neolib.SetClipBoard(self.dststr)
"""

class ConvUpperLowInClipBoard(ConvertBaseClipboard):
	def convContents(self):


		if maparg['option'] == 'up':
			self.dststr = self.dststr.upper()
		elif maparg['option'] == 'low':
			self.dststr = self.dststr.lower()

		None

class ConvDefineStringClipBoard(ConvertBaseClipboard):


	patttotal = r'([A-Za-z0-9_ ]+)(\t|\n|$)'
	pattcamel = r'([A-Za-z][a-z0-9]+)'
	#pattcamel = r'([A-Z][a-z0-9]*)'


	def InitValue(self):

		self.mapMakeArray = {
			"und": self.makeListFromUnderLine,
			"spc": self.makeListFromSpaceDiv,
			"cam": self.makeListFromCamelForm,
		}
		self.mapMakeString = {
			"und": self.convUnserLine,
			"und_row": self.convUnserLineLower,
			"cam": self.convCamelForm,

		}
		self.intype = ""
		self.outtype = ""

		if 'intype' in self.maparg:
			self.intype = maparg['intype']

		if 'outtype' in self.maparg:
			self.outtype = maparg['outtype']



		None


	def convCamelForm(self,listarray):
		newarra = []
		for tmp in listarray:
			hd = tmp[0:1].upper()
			boddy = tmp[1:].lower()
			newarra.append(hd+boddy)
		return "".join(newarra)

	def convUnserLine(self, listarray):
		newarra = []
		for tmp in listarray:
			newarra.append(tmp.upper())
		return "_".join(newarra)

	def convUnserLineLower(self, listarray):
		return self.convUnserLine(listarray).lower()

	def makeListFromUnderLine(self, orgstr):
		return orgstr.split("_")

	def makeListFromSpaceDiv(self, orgstr):
		return orgstr.split(" ")

	def makeListFromCamelForm(self, orgstr):
		result = re.findall(self.pattcamel,orgstr)
		for tmp in result:
			print(tmp[1])
			None
		return  list(map((lambda n:n),result))
	def test(self):
		res = self.convCamelForm(['abc', 'def', 'ghi'])
		print(res)
		res = self.convUnserLine(['abc', 'def', 'ghi'])
		print(res)

		res = self.convUnserLineLower(['abc', 'def', 'ghi'])
		print(res)

		resarray = self.makeListFromSpaceDiv('AAA BBB CCC')
		print(resarray)

		resarray = self.makeListFromUnderLine('AAA_BBB_CCC')
		print(resarray)
		resarray = self.makeListFromCamelForm('aaaBbbCcc')
		print(resarray)
	def inputOptions(self):

		inindex = int((input("input type 1.space div form 2.under line form 3.camel form: ")))



		mapIn = {
			1: "spc",
			2:"und",
			3:"cam",
		}

		if inindex not in mapIn :
			exit()

		outindex = int((input("output type 1.underline form  2.under line lower case form  3.camel form: ")))


		mapOut = {
			1: "und",
			2:"und_row",
			3:"cam",
		}

		if outindex not in mapOut:
			exit()


		self.intype = mapIn[inindex]
		self.outtype = mapOut[outindex]

		print(self.intype)
		print(self.outtype)





	def convContents(self):
		self.inputOptions()


		self.dststr = self.dststr.replace('\r\n','\n')
		results = re.findall(self.patttotal, self.dststr)

		if len(results) == 0 : exit()

		arrfunc = self.mapMakeArray[self.intype]
		strfunc =self.mapMakeString[self.outtype]

		retarra = []
		for tmp in results:
			#print(tmp[0])
			array = arrfunc(tmp[0])
			#print(array)
			resstr = strfunc(array )
			#print(resstr )
			retarra.append(resstr)
		self.dststr = "\r\n".join(retarra)




class PuttyRunNMove(BaseRunClass):
	cmd = 'putty.exe -load linux77'
	totalPuttyNum = 6;
	def refCode(self):
		print(__name__)

		yesterday = datetime.datetime(2016, 5, 12, 6, 45)
		ans_time = int(time.mktime(yesterday.timetuple()))
		print(ans_time)

		PyHANDLE = win32gui.FindWindow("PuTTY", None);


	def getSecondMonitorRect(self):

		list = win32api.EnumDisplayMonitors(None, None);

		h, h2, rect = list[len(list)-1]
		print(rect)

		return rect;


	def getExitedPuttyHandle(self):
		#print('enum window')
		nums = []
		def callbackGetPutty(pyHwnd, n):
			str = win32gui.GetClassName(pyHwnd)
			if str == "PuTTY":
				nums.append(pyHwnd)
				print(str)

		win32gui.EnumWindows(callbackGetPutty, 0)

		return nums;
	def generatePuttyWindow(self,needputty):

		for tmp in range(0, needputty):
			print('run putty')
			# os.system('putty.exe -load linux77')
			# subprocess.call('putty.exe -load linux77', shell=True)
			neolib.executeAsync(self.cmd)
			time.sleep(1)
	def reArrangePuttyWindows(self,puttyHwnds):


		rect = self.getSecondMonitorRect()
		print('Second Windows Rect',rect)

		Left,Top,Right,Bottom = rect;
		startX = Left;
		startY = Top;
		Width = Right - Left
		Height = Bottom - Top

		unitheight = int(Height / 3);
		unitwidth = int(Width / 3);


		count = 0
		print(startX, startY)
		numputty = len(puttyHwnds)
		mapRect = {}
		listpostiton =[(0,0),(1,0),(0,1),(1,1),(0,2),(1,2),(2,0),(2,1),(2,2)]
		for index in range(0,numputty-1):
			hwd = puttyHwnds[index]

			# realheight = unitheight
			# if index == numputty-1:
			# 	realheight = 2 * unitheight
			xindex,yindex = listpostiton[index]
			#yindex = int(index / 3);

			relativeX = unitwidth * xindex;
			relativeY = unitheight * yindex;

			mapRect[hwd] = relativeX, relativeY, unitwidth, unitheight

			print(relativeX, relativeY)

		#	win32gui.MoveWindow(hwd, startX + relativeX, startY + relativeY, unitwidth, realheight, 1);

			count += 1

		hwndLast = puttyHwnds[count]
		relativeX = unitwidth * 2;
		relativeY = unitheight * 0;
		mapRect[hwndLast] = relativeX, relativeY, unitwidth, Height

		print(mapRect)


		for hwd,value in mapRect.items():
			relativeX, relativeY, rwidth, rheight = value

			win32gui.MoveWindow(hwd, startX + relativeX, startY + relativeY, rwidth, rheight, 1);





	def doRun(self):
		#win32gui.EnumWindows(lambda n, m: print(n), 0)
		while True:
			print('Enum Windows')
			puttyHwnds = self.getExitedPuttyHandle();

			#win32gui.EnumWindows(self.callbackGetPutty, 0)
			countputty = len(puttyHwnds)
			print('countputty',countputty)
			if countputty >= self.totalPuttyNum: break;



			needputty = self.totalPuttyNum - countputty
			print('needputty',needputty)
			self.generatePuttyWindow(needputty)
			# for tmp in range(0,needputty):
			# 	print('run putty')
			# 	#os.system('putty.exe -load linux77')
			# 	#subprocess.call('putty.exe -load linux77', shell=True)
			# 	neolib.executeAsync(self.cmd)
			# 	time.sleep(1)

		print('move puttys')

		self.reArrangePuttyWindows(puttyHwnds)



class PuttyKIll(PuttyRunNMove):

	def doRun(self):
		for hWnd in self.getExitedPuttyHandle():
			neolib4Win.KillProcessFromHandle(hWnd)
			time.sleep(0.5)



		None




if __name__ != '__main__':
	exit()



maparg = neolib.listarg2Map(sys.argv)



mapfunction = {"strcpy": SetClipBoard(maparg),
			   "conv2java": ConvertMapCs2Java(maparg),
			   "makeNormalTxt": MakeNormalTxtInClipBoard(maparg),
				"convuplow": ConvUpperLowInClipBoard(maparg),
			   "convdeftype":ConvDefineStringClipBoard(maparg),
				"puttyrun":PuttyRunNMove(maparg),
			   "puttykill":PuttyKIll(maparg)

			   }


cmd = maparg["rt"]
print(maparg)
mapfunction[cmd]
mapfunction[cmd].doRun()
time.sleep(0.5)  # delays for 5 seconds
exit()
i = 5
while i > 0:
	time.sleep(1)  # delays for 5 seconds
	print(str(i) + "second left")
	i -= 1
