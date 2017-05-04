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
from enum import Enum

import xlwt
from xlutils.copy import copy as xlutils_copy
from copy import deepcopy as deep_copy


class COLIDX(Enum):
	num = 0
	depart = 1
	part = 2
	team = 3
	name  = 4
	inter_no = 5
	company_phnone = 6
	mobile_phone = 7
	email = 8
	pos = 9
	birtday = 10

class TARGETCOL(Enum):
	NAME=0
	COMPANY=1
	DEPART=2
	POSITION=3
	MEMO=4
	JOB_ADDR=5
	JOB_PHONENUM=6
	JOB_MAINNUM=7
	CELLPHONE=8
	EMAIL=9
	EMAILNAME=10
	CATAGORY=11

class HandleContact(neolib.NeoRunnableClasss):

	def InitRun(self):

		self.mapTitle =		collections.OrderedDict(
			[
				(TARGETCOL.NAME, ('이름', lambda row: row[COLIDX.name.value])),
				(TARGETCOL.COMPANY, ('회사', lambda row: 'ICTK')),
				(TARGETCOL.DEPART, ('부서', lambda row: '{0} {1} {2}'.format(row[COLIDX.depart.value], row[COLIDX.part.value], row[COLIDX.team.value]) )),
				(TARGETCOL.POSITION, ('직함', lambda row: row[COLIDX.pos.value])),
				(TARGETCOL.MEMO, ('메모', lambda row: row[COLIDX.birtday.value])),
				(TARGETCOL.JOB_ADDR, ('근무지 주소 번지', lambda row: '경기도 성남시 분당구 판교로 323 3층(삼평동,벤처포럼빌딩)')),
				(TARGETCOL.JOB_PHONENUM, ('근무처 전화', lambda row: row[COLIDX.company_phnone.value])),
				(TARGETCOL.JOB_MAINNUM, ('회사 대표 전화', lambda row: '')),
				(TARGETCOL.CELLPHONE, ('휴대폰', lambda row: "'"+row[COLIDX.mobile_phone.value])),
				(TARGETCOL.EMAIL, ('전자 메일 주소', lambda row: row[COLIDX.email.value])),
				(TARGETCOL.EMAILNAME, ('전자 메일 표시 이름', lambda row: row[COLIDX.name.value] + '(ICTK)')),
				(TARGETCOL.CATAGORY, ('범주 항목', lambda row: '직장')),

			]
		)
		self.mapTitleGoogle = collections.OrderedDict(self.mapTitle)
		self.mapTitleGoogle[TARGETCOL.NAME] = ('이름',lambda row: row[COLIDX.name.value] + '(ICTK)')





		None


	def fillOrder(self,rows):
		a = lambda x, y: x * y
		def prevset(rows,prevrows,idx):
			if len(prevrows) ==0 :return
			if rows[idx] != '' :return

			rows[idx] = prevrows[idx]


		prevrows = []
		for tmp in rows:


			if len(prevrows) ==0 :
				prevrows = tmp
				continue
			if tmp[0] == '중국':
				asd = 0
			prevset(tmp, prevrows, 0)
			prevset(tmp, prevrows, 1)
			prevset(tmp, prevrows, 2)
			prevset(tmp, prevrows, 3)

			prevrows = tmp

		return


	def getRowsFromXlsFile(self,xlsfile):
		xl_workbook = xlrd.open_workbook(xlsfile)
		sheet_names = xl_workbook.sheet_names()
		print('Sheet Names', sheet_names)
		xl_sheet = xl_workbook.sheet_by_name('ICTK 연락처')
		print('Sheet name: %s' % xl_sheet.name)

		rows = []
		rows1 = []
		for tmp in [aaa for aaa in xl_sheet.get_rows()][3:]:
			rows.append([col.value for col in tmp[1:10]])
			rows1.append([col.value for col in tmp[10:20]])

		self.fillOrder(rows)
		self.fillOrder(rows1)

		rows.extend(rows1)
		return  rows

	def fnfilter(self,aaa):
		res = re.match(r'^[a-zA-Z0-9\.]+@ictk(-china)*\.com', aaa[8])
		if res == None: return False
		return True

	def processAfter(self,rows):
		lastidx = 0;
		for tmp in rows:
			idx = -1
			for col in tmp:
				idx += 1
				if type(col) == float:
					tmp[idx] = int(col)

				if type(col) == str:
					col = col.replace('\n','')
					col = col.replace('\xa0', '')

					#if idx != COLIDX.name.value:
					col = col.replace(' ', '')

					tmp[idx] = col
			if 	type(tmp[COLIDX.num.value]) == int :
				lastidx = tmp[COLIDX.num.value]
		#patt = r'((?:[\w]{3})|(?:\w\s+\w\s+\w))(?:\s+(COO|차장|이사|팀장|대리|수석|책임|선임|소장|주임|상무|실장|전임|부사장|과장))*\s*(\d{2}\.\d{2}\((?:양|음)\))'
		patt =r'([가-힣]{2,3})(COO|차장|이사|팀장|대리|수석|책임|선임|소장|주임|상무|실장|전임|부사장|과장)*\s*(\d{2}\.\d{2}\((?:양|음)\))'
		for tmp in rows:
			if tmp[COLIDX.num.value] in ['중국','룩셈부르크']:
				lastidx += 1
				tmp[COLIDX.depart.value] = tmp[COLIDX.num.value]
				tmp[COLIDX.depart.company_phnone.value] = tmp[COLIDX.inter_no.value]
				tmp[COLIDX.num.value] = lastidx
			name = tmp[COLIDX.name.value]
			res = re.findall(patt,name)
			name,pos,birtday = res[0]

			tmp[COLIDX.name.value] = name
			departname = tmp[COLIDX.depart.value]

			if pos == '' and departname in ['부회장','부대표이사','감사','본부장','대표이사본부장']:
				pos = tmp[COLIDX.depart.value]
			tmp.extend([pos,birtday])
			print(name)

	def MakeNewRows(self,mapTitle,rows):
		newrows = []

		newrows.append([v[0] for k,v in self.mapTitle.items()])

		print(newrows)

		for tmp in rows:
			nrow =[]
			for k, v in mapTitle.items():
				nrow.append(v[1](tmp))
			newrows.append(nrow)
			print(nrow)
		return newrows

	def SaveXls(self,rows,filename):
		workbook = xlwt.Workbook()

		sheet = workbook.add_sheet("Sheet Name")
		x = 0
		y = 0
		for tmp in rows:
			x = 0
			for col in tmp:
				sheet.write(y,x,col)  # row, column, value
				x += 1
			y += 1

		workbook.save(filename)

	def SaveCsv(self,rows,filename):
		with open(filename, 'w',newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for tmp in rows:
				writer.writerow(tmp)


	def doRun(self):

		xlspath = self.maps['xlsfile']
		rows = self.getRowsFromXlsFile(xlspath)

		rows = list(filter(self.fnfilter, rows))

		self.processAfter(rows)

		rows = sorted(rows, key=lambda student: student[0])

		newrows = self.MakeNewRows(self.mapTitle,rows)
		#self.SaveXls(newrows,'contact.xls')
		self.SaveCsv(newrows, 'contact.csv')

		newrows = self.MakeNewRows(self.mapTitleGoogle, rows)
		self.SaveCsv(newrows, 'contact_google.csv')
		#self.SaveXls(newrows, 'contact_google.xls')




if __name__ != '__main__':
	exit()

HandleContact().Run()




#ret = [tuple([tmp.value for tmp in row][1:]) for row in rows]

# print(sys.argv)
# maps = {}
# lists = sys.argv
# length = len(lists)
# print(lists)
#
# maps = {tmp[1:]:''  for tmp in lists if tmp.startswith('-')}
#
# for key,val in maps.items():
# 	idx = lists.index('-'+key)
# 	print(idx)
# 	if idx + 1 >= length :continue
# 	if lists[idx + 1].startswith('-') :continue
#
# 	maps[key] = lists[idx+1]
#print(maps)