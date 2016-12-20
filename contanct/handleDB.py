import re
import requests
import datetime
import shutil
import sys
import time
import gc
import  json
import time
import codecs
import base64
import logging
import collections
from logging import handlers
import xlrd
import csv

import neolib.neolib as neolib
import neolib.db as neodb

from enum import Enum

import xlwt
from xlutils.copy import copy as xlutils_copy
from copy import deepcopy as deep_copy

class CreateTableAnd(neodb.MakeCreateTableFor):
	xlsDbFile = "CONTACT_TABLE정보.xlsx"
	def doRun(self):
		ret = self.makeMapFromExcel(self.xlsDbFile)
		self.strlines = self.makeSqlDropAndCreate(ret,self.createTableForm,self.fieldForm)
		neolib.StrToFile(self.strlines, "table/TABLE.SQL")
		self.strlines = self.makeSqlDropAndCreate(ret, self.dropTableForm, '')
		neolib.StrToFile(self.strlines, "table/DROP.SQL")

		None



if __name__ != '__main__':
	exit()

CreateTableAnd().Run()