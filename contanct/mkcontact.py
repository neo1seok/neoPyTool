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
import neolib.neolib as neolib



if __name__ != '__main__':
	exit()
maps = neolib.getMapsFromArgs(sys.argv)

xlspath = maps['xlsfile']

# fname = 'D:/PROJECT/toolrnd/DeviceTesterSystem/DOCS/DB설계서_161107.xlsx'

# Open the workbook
xl_workbook = xlrd.open_workbook(xlspath)
sheet_names = xl_workbook.sheet_names()
print('Sheet Names', sheet_names)
xl_sheet = xl_workbook.sheet_by_name('ICTK 연락처')
print('Sheet name: %s' % xl_sheet.name)
# Or grab the first sheet by index
#  (sheets are zero-indexed)
#
# xl_sheet = xl_workbook.sheet_by_index(0)
# print ('Sheet name: %s' % xl_sheet.name)

# Pull the first row by index
#  (rows/columns are also zero-indexed)
#
# row = xl_sheet.row(1)  # 1st row
# rows = [tmp for tmp in xl_sheet.get_rows()][2:]
# print(rows)
# print([[tmp.value for tmp in row][1:] for row in [tmp for tmp in xl_sheet.get_rows()][2:]])
# for row in rows:
# 	print([tmp.value for tmp in row][1:])
# # print("\t".join(vals.value for vals in [tmp.value	for tmp in row][1]))
rows = []
for tmp in [aaa for aaa in xl_sheet.get_rows()][3:]:

	rows.append([ col.value for col in tmp[1:10]])
	rows.append([col.value for col in tmp[10:19]])

def fnfilter(aaa):

	if ''.join([str(tmp) for tmp in aaa]) == '' :return  False
	print(type(aaa[0]) ,float)
	if type(aaa[0]) != float  :return  False

	return True
rows = list(filter( fnfilter,rows))
def numeric_compare(x, y):

	return x[0] - y[0]

sorted(rows, cmp=numeric_compare)
print(rows)
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
print(maps)