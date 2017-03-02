import datetime
import re
import sys
import time
import win32api
import win32gui


import neolib.neolib as neolib
import neolib.neolib4Win as neolib4Win

import win32api
import inspect
import requests
import simplejson as json
import win32gui
import win32con
import time
from  math import cos, sin, pi
from time import ctime
import ntplib
from time import ctime

class BaseRunClass(neolib.NeoRunnableClasss):
	class_name = ""
	desc = ""
	objects = {}

	def __init__(self, maparg):

		self.maparg = maparg
		self.InitValue()

	def InitValue(self):
		#parser = optparse.OptionParser('usage %prog -i <input_file>')
		None
	#
	# def doRun(self):
	# 	print('a')
	#
	# def InitValue(self):
	# 	None


class SetClipBoard(BaseRunClass):
	mapstr = {"greeting": "안녕하십니까? ICTK 신원석입니다.\r\n\r\n\r\n오늘도 좋은 하루 되십시오.\r\n감사합니다.",
			  "greeting2": "개발1실 신원석입니다.\r\n\r\n\r\n수고하십시오.",
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

		# self.mapMakeArray = {
		# 	"und": self.makeListFromUnderLine,
		# 	"spc": self.makeListFromSpaceDiv,
		# 	"cam": self.makeListFromCamelForm,
		# }
		# self.mapMakeString = {
		# 	"und": self.convUnserLine,
		# 	"und_row": self.convUnserLineLower,
		# 	"cam": self.convCamelForm,
		#
		# }
		self.intype = ""
		self.outtype = ""

		if 'intype' in self.maparg:
			self.intype = maparg['intype']

		if 'outtype' in self.maparg:
			self.outtype = maparg['outtype']



		None

	#
	# def convCamelForm(self,listarray):
	# 	newarra = []
	# 	for tmp in listarray:
	# 		hd = tmp[0:1].upper()
	# 		boddy = tmp[1:].lower()
	# 		newarra.append(hd+boddy)
	# 	return "".join(newarra)
	#
	# def convUnserLine(self, listarray):
	# 	newarra = []
	# 	for tmp in listarray:
	# 		newarra.append(tmp.upper())
	# 	return "_".join(newarra)
	#
	# def convUnserLineLower(self, listarray):
	# 	return self.convUnserLine(listarray).lower()
	#
	# def makeListFromUnderLine(self, orgstr):
	# 	return orgstr.split("_")
	#
	# def makeListFromSpaceDiv(self, orgstr):
	# 	return orgstr.split(" ")
	#
	# def makeListFromCamelForm(self, orgstr):
	# 	result = re.findall(self.pattcamel,orgstr)
	# 	for tmp in result:
	# 		print(tmp[1])
	# 		None
	# 	return  list(map((lambda n:n),result))
	# def test(self):
	# 	res = self.convCamelForm(['abc', 'def', 'ghi'])
	# 	print(res)
	# 	res = self.convUnserLine(['abc', 'def', 'ghi'])
	# 	print(res)
	#
	# 	res = self.convUnserLineLower(['abc', 'def', 'ghi'])
	# 	print(res)
	#
	# 	resarray = self.makeListFromSpaceDiv('AAA BBB CCC')
	# 	print(resarray)
	#
	# 	resarray = self.makeListFromUnderLine('AAA_BBB_CCC')
	# 	print(resarray)
	# 	resarray = self.makeListFromCamelForm('aaaBbbCcc')
	# 	print(resarray)
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

		classconv = neolib.ConvStringForm(intype=self.intype,outtype=self.outtype)

		# arrfunc = self.mapMakeArray[self.intype]
		# strfunc =self.mapMakeString[self.outtype]

		retarra = []
		for tmp in results:
			#print(tmp[0])
			#array = arrfunc(tmp[0])
			#print(array)
			#resstr = strfunc(array )
			#print(resstr )
			resstr = classconv.ConvertString(tmp[0])
			retarra.append(resstr)
		self.dststr = "\r\n".join(retarra)




class PuttyRunNMove(BaseRunClass):
	cmd = 'putty.exe -load linux77'
	totalPuttyNum = 6;

	def InitValue(self):
		#parser = optparse.OptionParser('usage %prog -i <input_file>'
		# )

		self.session =neolib.get_safe_mapvalue(self.maparg,'session')
		self.cmd = 'putty.exe -load %s'%self.session

		None

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


		for hwnd,value in mapRect.items():
			relativeX, relativeY, rwidth, rheight = value
			print(hwnd)
			win32gui.SetWindowPos(hwnd, 0,startX + relativeX, startY + relativeY, rwidth, rheight, 0x0040);
			#HWND = win32gui.SetActiveWindow(hwnd)
			print(hwnd)
			#win32gui.SetForegroundWindow(hwnd)


			#win32gui.MoveWindow(hwd, startX + relativeX, startY + relativeY, rwidth, rheight, 1);
			#win32gui.ShowWindow(hwd, 5)





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
	def InitValue(self):
		print("PuttyKIll")

		None

	def doRun(self):
		for hWnd in self.getExitedPuttyHandle():
			neolib4Win.KillProcessFromHandle(hWnd)
			time.sleep(0.5)



		None


class drawMousePos(BaseRunClass):
	def InitValue(self):


		# points = [pos,(pos[0]-100,pos[1]-100),(pos[0]-100,pos[1]+100),(pos[0]+100,pos[1]+100),(pos[0]+100,pos[1]-100)]
		self.points = self.make_circle(100,100)
		self.pointssmall = self.make_circle(10, 100)
		# self.pointssmall = []
		# r = 100;
		# unitrad = 2 * pi / 100.0
		#
		# for idx in range(100):
		# 	rad = idx * unitrad
		# 	posunit = (int(r * cos(rad) ), int(r * sin(rad)))
		# 	self.points.append(posunit)
		# r = 10;
		# for idx in range(100):
		# 	rad = idx * unitrad
		# 	posunit = (int(r * cos(rad) ), int(r * sin(rad)))
		# 	self.pointssmall.append(posunit)

		None
	def accept_plus(self,ss):
		if ss < 0: return 0
		return ss
	def make_circle(self,r,unitnum):
		points = []
		unitrad = 2 * pi / unitnum
		for idx in range(100):
			rad = idx * unitrad
			posunit = (int(r * cos(rad) ), int(r * sin(rad)))
			points.append(posunit)
		return points



	def shift_points(self,points,shiftpos):
		(mx,my)=shiftpos
		return [(self.accept_plus(x + mx), self.accept_plus(y + my)) for (x, y) in points]

	def doRun(self):
		(mx,my) = win32gui.GetCursorPos()
		#print(self.points)
		self.points = self.shift_points(self.points,(mx,my))
		self.pointssmall = self.shift_points(self.pointssmall, (mx, my))

		#print(self.points)
		dc = win32gui.GetDC(None)
		hpen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))
		horg = win32gui.SelectObject(dc, hpen)
		win32gui.Polyline(dc, self.points)
		win32gui.Polyline(dc, self.pointssmall)
		win32gui.SelectObject(dc, horg)
		win32gui.DeleteObject(hpen)
		win32gui.ReleaseDC(None, dc)

		time.sleep(1)
		win32gui.InvalidateRect(None, None, True)

class UpdaateSystemTime(BaseRunClass):
	def doRun(self):
		c = ntplib.NTPClient()
		response = c.request('time.google.com', version=3)
		
		print(response.offset)
		print(response.version)
		print("서버시간:",ctime(response.tx_time))
		print("시스템시간:",ctime(time.time()))
		
		neolib4Win._win_set_time(datetime.datetime.fromtimestamp(int(response.tx_time+response.root_delay)).timetuple())
		print("시스템시간:",ctime(time.time()))
		
		print(response.tx_time-time.time())


		print(ntplib.leap_to_text(response.leap))

		print(response.root_delay)

		print(ntplib.ref_id_to_text(response.ref_id))
		
		
	def Test(self):

		time_tuple = (2008, 11, 12, 13, 51, 18, 2, 317, 0)

		dt_obj = datetime.datetime(*time_tuple[0:6])

		neolib4Win._win_set_time(dt_obj.timetuple())
		  
		#exit()
		#print(datetime.datetime.now())
		print(datetime.datetime.now().timetuple()[0:6])
		#print(datetime.datetime(datetime.datetime.now().timetuple()))
		print(time.time())
		print(ctime())
		self.doRun()
		
		# #exit()
		# response = c.request('europe.pool.ntp.org', version=3)
		# print(response.offset)
		# print(response.version)
		#
		# print(ctime(response.tx_time))
		# print(ctime(time.time()))
		#
		#
		# print("서버시간:",datetime.datetime.fromtimestamp(int(response.tx_time)).strftime('%Y-%m-%d %H:%M:%S'))
		# print("시스템시간:",datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		# neolib4Win._win_set_time(datetime.datetime.fromtimestamp(int(response.tx_time)).timetuple())
		# print("시스템시간:",datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))



	None

print("start")

if __name__ == '__main__':

	maparg = neolib.listarg2Map(sys.argv)

	mapfunction = {"strcpy": SetClipBoard,
				   "conv2java": ConvertMapCs2Java,
				   "makeNormalTxt": MakeNormalTxtInClipBoard,
				   "convuplow": ConvUpperLowInClipBoard,
				   "convdeftype": ConvDefineStringClipBoard,
				   "puttyrun": PuttyRunNMove,
				   "puttykill": PuttyKIll,
				   "drawMousePos": drawMousePos,

				   }

	cmd = maparg["rt"]
	print(maparg)
	runobj = mapfunction[cmd](maparg)
	runobj.doRun()
	time.sleep(0.5)  # delays for 5 seconds
	exit()
	i = 5
	while i > 0:
		time.sleep(1)  # delays for 5 seconds
		print(str(i) + "second left")
		i -= 1





