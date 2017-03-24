import neolib.neolib as neolib
import neolib.db as neodb
import time

import  simplejson as json
import re
import collections


class CreateClass(neodb.MakeDataFieldsClass):
	xlsDbFile = "rsc/DB설계서.xlsx"

	def doRun(self):
		self.convert();





if __name__ != '__main__':
	exit()


CreateClass().Run()