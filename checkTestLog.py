import neolib
import re
import sys


class CheckIUST100TestLog(neolib.NeoRunnableClasss):
	def __init__(self, maparg):
		self.maparg = maparg
		self.InitValue()


	def doRun(self):
		obj1 = re.compile(r'((TEST START)\s*:\s*(.+))|((TEST RESULT)\s*:\s*(.+))')
		# obj2 = re.compile(r'TEST START\s*:\s*(.+)')
		path = self.maparg['path']

		print(path)

		str = neolib.StrFromFile(path)


		start = ''

		for tmp in re.findall(obj1, str):
			if tmp[0] != '':
				tag = tmp[1]
				result = tmp[2]
				start = result
			else:
				tag = tmp[4]
				result = tmp[5]
				print(start,':', result)


		None

	def InitValue(self):
		None

if __name__ != '__main__':
	exit()
maparg = neolib.listarg2Map(sys.argv)
CheckIUST100TestLog(maparg).Run()