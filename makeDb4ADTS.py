import os
import re
import shutil
import socket
import win32api
import win32gui
import win32con
import time
import datetime
import sys
import glob

#import json

import win32clipboard
import neolib
import base64
import pymysql
import http.client

import hashlib
import gzip
import random
import ssl
import string

import pymysql
import sys

import requests

import  simplejson as json
import collections

import neolib4Win

class dbHandleing:
	def __init__(self,**kwargs):
		self.conn = pymysql.connect(**kwargs)
		self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

	@staticmethod
	def makeMapMapDBFromListMapDB(key,listMapDB):
		return collections.OrderedDict([(tmprow[key],tmprow ) for tmprow in listMapDB])

	def select(self,sql):
		print(sql)
		self.cur.execute(sql)
		return self.cur.fetchall()
	def selectToMap(self,key,sql):
		return self.makeMapMapDBFromListMapDB(key,self.select(sql))

	def excute(self,sql):
		print(sql)
		self.cur.execute(sql)

	def lastSeq(self,tablename):

		sql = "SELECT seq FROM {0} order by seq desc limit 1 ;".format(tablename)
		mapres = self.select(sql)
		if len(mapres) == 0: return 0

		return int(mapres[0]['seq'])

	def insert(self,table,prefix,maprow,lastseq):




		return self.insertList(table,prefix,[maprow],lastseq)



	def insertList(self,table,prefix,listmaprow,lastseq):
		if len(listmaprow)  == 0: return
		maprow = listmaprow[0]

		arraycol = [key if key != 'index' else '`index`' for key,vlaue in maprow.items()]

		lastseq+=1



		sqldstfmt = "INSERT {0} (   seq  ,{1}_uid  ,{2}  ,updt_date  ,reg_date  ) VALUES \n{3}"
		# 0:table 1:prefix 2:col araay 3:values
		sqlvalueContents = "({1}  ,'{0}_{1}',{2},now(),now())"
		# 0:prefix 1:seq 2: values
		values = []
		for maprow in listmaprow:
#			arrayval = list(map(self.mapfunction,maprow.items()))
			arrayval = ["'%s'" % vlaue for key, vlaue in maprow.items()]

			values.append(sqlvalueContents.format(prefix,lastseq,",".join(arrayval)))
			lastseq+=1

		sql = sqldstfmt.format(table,prefix,",".join(arraycol),",\n".join(values))
		print(sql)
		self.cur.execute(sql);

		return lastseq

	def mapfunction(self, tmp):
		key, value = tmp

		if type(value) == str:
			#print(type(value))
			value = value.replace("'", "\\'")
		return "'%s'" % value

		#0:table 1:prefix 2:seq 3:col araay 4:values

		sql = sqldstfmt.format(table,prefix,lastseq,",".join(arraycol),",".join(arrayval))

		self.cur.execute(sql);


		return lastseq+1

	def deleteTable(self,table):
		self.cur.execute('DELETE FROM %s;'%table)


class BaseMySQLRunnable(neolib.NeoRunnableClasss):
	ignorenames = ['Message Type', '거래구분코드']



	def test(self,**kwargs):
		for key,value in kwargs.items():
			print(key,value)
		None

	def test2(self,**kwargs):
		self.test(**kwargs)
		None

	def InitRun(self):

		# self.test2(aaa='1',aaa2='2')


		self.listmap = []

		# self.conn = pymysql.connect(host='localhost', port=3306, user='neo1seok', passwd='tofhdna1pi',
		# 					   db='test_smartro', charset='utf8')
		#
		#
		#
		# self.conndst = pymysql.connect(host='192.168.0.75', port=3306, user='ictk', passwd='#ictk1234',
		# 						  db='adts', charset='utf8')
		#
		# self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
		#
		# self.curdst = self.conndst.cursor(pymysql.cursors.DictCursor)

		self.olddbHD = dbHandleing(host='localhost', port=3306, user='neo1seok', passwd='tofhdna1pi',db='test_smartro', charset='utf8')
		#self.dstdbHD = dbHandleing(host='192.168.0.75', port=3306, user='ictk', passwd='#ictk1234',	  db='adts', charset='utf8')
		self.dstdbHD = dbHandleing(host='localhost', port=3306, user='ictk', passwd='#ictk1234', db='adts',
								   charset='utf8')

		None

	def doRun(self):
		self.strlines = ""

		self.makeMap4Type()

		self.makeMap4Protocol()

		self.mainProcess()

		#print(self.strlines)

		None

	def endRun(self):
		fb = open('out.txt', 'wb')
		fb.write(self.strlines.encode())
		fb.close()

		neolib4Win.SetClipBoard(self.strlines)

		self.olddbHD.conn.close()
		self.dstdbHD.conn.close()
		neolib.NeoRunnableClasss.endRun(self)


	def makeMapMapDBFromListMapDB(self,key,listMapDB):
		return dbHandleing.makeMapMapDBFromListMapDB(key,listMapDB)
		# return collections.OrderedDict([(tmprow[key],tmprow ) for tmprow in listMapDB])
		#
		# return {tmprow[key]:tmprow  for tmprow in listMapDB}
		#
		# newmap = {}
		# for tmprow in listMapDB:
		# 	newmap[tmprow[key]] = tmprow
		# return newmap;

	def makeMap4Protocol(self):
		mapprotocol = self.olddbHD.select(	"SELECT seq, uid, protocol, direction, servicecode, data, devtype FROM maindev_protocol where devtype = 'V100_EN07'")
		self.mapOldDBMainProtocol = collections.OrderedDict([(row['protocol'] + row['direction'],row) for row in mapprotocol])
		#self.mapOldDBMainProtocol = {row['protocol'] + row['direction']:row for row in mapprotocol}
		return

		self.mapOldDBMainProtocol =collections.OrderedDict()

		for row in mapprotocol:
			self.mapOldDBMainProtocol[row['protocol'] + row['direction']] = row

	def makeMap4Type(self):
		self.mapOldDBMainType = self.olddbHD.selectToMap('id',"SELECT id, name, type, length, chartype, options, devtype FROM maindev_type where devtype = 'V100_EN07'")
		#self.mapOldDBMainType = self.makeMapMapDBFromListMapDB('id', maptype)

	def mainProcess(self):
		None


	def append(self, str):
		print(str)
		self.strlines += str

		self.strlines += "\n"

	def appendA(self, *args,**kwargs):

		self.strlines += '\t'.join(args)
		print(self.strlines)

		self.strlines += "\n"


	sentencepatt = r'G([0-9]+):(F|T):([0-9A-Za-z가-힣^.,_$=\-+()*\^ ]*)\^\\'

	def makeMapJustValue(self, result_list):
		mapresultvalus = collections.OrderedDict()
		for id, VFT, value in result_list:
			strid = str(int(id))
			name = self.mapOldDBMainType[strid]['name']


			sepoptions = self.mapOldDBMainType[strid]['options'].split('|')

			if name in self.ignorenames:
				continue
			if VFT == 'T':
				value = 'EMPTY' if 'O' not in sepoptions else 'REMOVE'

			mapresultvalus[name] = value

			None

		return mapresultvalus


	def ConvertFromSentence(self,mapresultvalus,sentence):

		result_list = re.findall(self.sentencepatt, sentence)

		remove = re.sub(self.sentencepatt, "", sentence)

		for k,v in self.makeMapJustValue(result_list).items():
			mapresultvalus[k] = v;
		return (mapresultvalus,remove)

	def getValue(self, key, maps):
		if key not in maps: return ''
		return maps[key]

	#
	#
	#
	#
	# def insert(self,table,prefix,maprow,lastseq):
	#
	# 	arraycol = [key for key,vlaue in maprow.items()]
	# 	arrayval = [ "'%s'"%vlaue for key, vlaue in maprow.items()]
	#
	#
	# 	sqldstfmt = "INSERT {0} scenario(   seq  ,{1}_uid  ,{3}  ,updt_date  ,reg_date  ,comment) " \
	# 				"VALUES ({2}  ,'{1}_{2}',{4},now(),now(),'')"
	# 	#0:table 1:prefix 2:seq 3:col araay 4:values
	#
	# 	sql = sqldstfmt.format(table,prefix,lastseq,",".join(arraycol),",".join(arrayval))
	#
	# 	self.curdst.execute(sql);
	#
	#
	# 	return lastseq+1

	def appendLine(self, **kwargs):
		mapresult = collections.OrderedDict()
		for tmp in self.cols:
			mapresult[tmp] = ''

		for key,value in kwargs.items():
			if type(value) == str:
				value = value.replace("'", "\\'")
			mapresult[key] = value

		self.listmap.append(mapresult)

class BaseTableInput(BaseMySQLRunnable):
	dsttable = "";
	prefix = ""
	colline = ""

	def mainProcess(self):
		self.dstdbHD.deleteTable(self.dsttable)
		self.cols = re.split(r',\s*',self.colline)
		self.listmap = []


		self.processInserValues()

		for row in self.listmap:
			print(row)

		self.processInserToDB()

		None


	def processInserValues(self):
		None

	def processInserToDB(self):
		lastseq = self.dstdbHD.lastSeq(self.dsttable)
		self.dstdbHD.insertList(self.dsttable, self.prefix, self.listmap, lastseq)



class MakePacketDateType(BaseTableInput):
	dsttable = "packet_data_type"
	colline = "name, length, variation, value_encoding, char_range, fixed_value, param, param_ext"
	prefix = "pdt"

	def processInserValues(self):

		self.appendLine(name="STX", length="1", value_encoding='HEX', fixed_value="02")
		self.appendLine(name="ETX", length="1", value_encoding='HEX', fixed_value="03")
		self.appendLine(name="CRC", length="2", value_encoding='HEX')

		for key, value in self.mapOldDBMainType.items():

			self.index = 0
			self.processDataTypes('',value)

		None


	def processDataTypes(self, servicecode,datamap):
		name = datamap['name']
		length = datamap['length']
		options = datamap['options']
		chartype = datamap['chartype']

		types = options.split('|')
		strv = ''
		if 'V' in types:                strv = 'TRUE'
		mapparam = collections.OrderedDict()

		order = '0'
		value = ''
		if name == '전문길이':
			order = '1'
			mapparam["RUN_POS"] = "END_RUN"

		elif name == 'Message Type':
			value = servicecode[0:4]
			None
		elif name == '거래구분코드':
			value = servicecode[4:6]
			None

		option = ''
		if 'O' in types:
			mapparam["OPTION"] = "TRUE"

			option = '{"TYPE":"OPTION"}'
		# return


		if 'F' not in types:
			if 'SI' not in types:
				mapparam["START_TAG"] = "FS"
				#self.appendLine(name="FS", length="1", encoding='HEX', value="1C",param=strparam,)
			strscript = 'CALCL_ENGTH'

		if 'SI' in types:
			mapparam["START_TAG"] = "SI"
			#self.appendLine(name="SI", length="1", encoding='HEX', value="0F",param=strparam,)
		strparam = ''
		if len(mapparam) > 0:
			strparam = json.dumps(mapparam, ensure_ascii=False)

		self.appendLine(name=name, length=length, variation=strv, value_encoding='ASCII', char_range=chartype, fixed_value=value,
						param=strparam, param_ext=order)


class MakePacket(BaseTableInput):
	dsttable = "packet";
	prefix = "pck"
	colline = "name, type, discription, script_file, make_class, confirm_class"
	def makePacketName(self,protocol,direction):
		tail = '수신' if direction == 'D2A'  else '송신'

		return protocol + " " + tail;

	def processInserValues(self):
		for key, value in self.mapOldDBMainProtocol.items():
			protocol = value['protocol']
			direction = value['direction']
			name = self.makePacketName(protocol,direction)

			self.appendLine(name=name,type="MAIN",script_file='smatro_sc.py',make_class="MAKE_PACKET_MAIN", confirm_class="CONFRIM_PACKET_MAIN")

		None

class MakePacketDataUnit(MakePacket):
	dsttable = "packet_data_unit";
	colline = "pck_uid, index, pdt_uid, def_value,comment"
	prefix = "pdu"

	def processInserValues(self):
		mapPacket = self.dstdbHD.selectToMap("name","SELECT seq, pck_uid, name, type, discription, script_file, make_class, confirm_class FROM adts.packet;")
		self.mapType = self.dstdbHD.selectToMap("name", "SELECT seq, pdt_uid, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment FROM adts.packet_data_type;")
		for key, row in self.mapOldDBMainProtocol.items():
			index = 0;
			datas = row['data']
			servicecode = row['servicecode']
			protocol = row['protocol']
			direction = row['direction']
			packetName = self.makePacketName(protocol,direction)
			pck_uid = mapPacket[packetName]['pck_uid']





			# self.append('KEY: {0} {1}'.format(self.protocol,self.direction))

			self.index = 0
			self.appendSel(pck_uid,'STX')

			for tmpindex in datas.split('|'):
				typename = self.mapOldDBMainType[tmpindex]['name']
				value = ''
				if typename == 'Message Type':
					value = servicecode[0:4]

				elif typename == '거래구분코드':
					value = servicecode[4:6]

				self.appendSel(pck_uid, typename,value)

			self.appendSel(pck_uid, 'ETX')
			self.appendSel(pck_uid, 'CRC')



		None

	def appendSel(self,pck_uid,typename,defvalue=''):
		print(typename)
		pdt_uid = self.mapType[typename]['pdt_uid']
		self.appendLine(pck_uid=pck_uid, index=self.index, pdt_uid=pdt_uid, def_value=defvalue,comment=typename)
		self.index += 1






#이 클래스는 스마트로의 스크립트 정보를 이용하여
#새로운 커맨드 라인을 만드는 클래스이다.
#rsc/cmdmappingTable.txt 에 instruction mapping 정보가
#뉴라인 탭 형태의 테이블 정보로 들어 있다.

class MakeScenario(BaseTableInput):
	dsttable = "scenario"
	prefix = "sce"
	colline = "scg_uid, name, discription, profile_sc, profile_reset_sc, script_file, classname"

	def processInserValues(self):
		listmapcriptsub = self.olddbHD.selectToMap('scriptid',
			"SELECT B.scriptid, title, script, objective, category, subcategory, caseid, testcase, B.profilename,  C.description "
			"FROM script_sublist B,profile_profile_sublist C where B.devtype = C.devtype and B.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용');")

		for key,row in listmapcriptsub.items():
			objective = row['objective']

			self.appendLine(name=key,discription=objective,script_file='smatro_sc.py',classname='SMARTRO_SC')



		None

class MakeScenarioLine(BaseTableInput):
	dsttable = "scenario_line"
	prefix = "scl"
	colline = "sce_uid, index, method, title, param, param_ext, pck_uid,comment"

	def processInserValues(self):

		#self.makeJsonFile()
		strjson = neolib.StrFromFile('rsc/mapScriptPerScenarioAndMethodLine.json')
		self.listmapcript = json.loads(strjson);

		mapdstScenario = self.dstdbHD.selectToMap('name',"SELECT seq, sce_uid, scg_uid, name, discription, profile_sc, profile_reset_sc, script_file, classname, updt_date, reg_date, comment FROM adts.scenario;")
		mapmapmethodline = self.dstdbHD.selectToMap('name',"SELECT seq, pck_uid, name, type, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment FROM adts.packet;")


		mapret =  self.makeMapCmdFromInputSrc()

		prevscriptid = ''
		curuid = ''

		mapScriptPerScenarioAndMethodLine = {}
		index = 0;
		for tmprow in self.listmapcript:
			pck_uid = ''
			instruction = tmprow['instruction']
			scriptid = tmprow['scriptid']
			protocol = tmprow['protocol']
			sce_uid = mapdstScenario[scriptid]['sce_uid']

			if scriptid != prevscriptid:
				index = 0
			prevscriptid = scriptid
			if instruction not in mapret: continue

			cond, newinst, title, param, param_ext, input_value = mapret[instruction]

			title = self.ConvertValue(title, tmprow, input_value)
			param = self.ConvertValue(param, tmprow, input_value)

			if "전문" in instruction:
				map = self.ConvertFromSentence(collections.OrderedDict(), param)[0]
				param = json.dumps(map, ensure_ascii=False)

				if "수신" in instruction:
					packetname = protocol + " 수신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']
					self.appendLine(sce_uid=sce_uid, index=index, method ='RECV' ,title='수신', param='$PORT00')
					index+=1
					self.appendLine(sce_uid=sce_uid, index=index, method='CONFIRM_PACKET', title=title, param=packetname ,pck_uid=pck_uid,comment= param )
					None
				elif "송신" in instruction:
					packetname = protocol + " 송신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']
					self.appendLine(sce_uid=sce_uid, index=index, method='MAKE_PACKET', title=title, param=packetname ,pck_uid=pck_uid,comment=param)
					index += 1
					self.appendLine(sce_uid=sce_uid, index=index, method='SEND', title='송신', param='$PORT00')
					None
				index += 1
				continue

			self.appendLine(sce_uid=sce_uid,method=newinst,index=index,title=title,param=param,param_ext=param_ext	)
			index+=1

	def processInserToDBa(self):
		lastseq = self.dstdbHD.lastSeq(self.dsttable)
		for tmp in self.listmap:
			self.dstdbHD.insert(self.dsttable, self.prefix, tmp, lastseq)
			lastseq+=1



		None





	def makeMapCmdFromInputSrc(self):
		mapret = {}
		strmenu = neolib.StrFromFile('rsc/cmdmappingTable.txt')
		mapobj = map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
		listmenu = list(filter(lambda x: len(x)>4, mapobj))
		for cond,inst,newinst,title,param,param_ext,input_value in listmenu:
			mapret[inst] = cond,newinst,title,param,param_ext,input_value
		return mapret

	def ConvertValue(self,value,mapRows,input_value):
		arrayparam = json.loads(input_value)
		newarrayparam = []
		for tmp in arrayparam:
			newarrayparam.append(mapRows[tmp])


		return  value.format(* newarrayparam)


	def makeJsonFile(self):
		self.listmapcript = self.olddbHD.select(
			"SELECT A.scriptid, instruction, delay, protocol, sentence, etc, direction,B.caseid,B.objective,A.devtype,B.profilename,C.description FROM test_smartro.script_maininfo A,test_smartro.script_sublist B,test_smartro.profile_profile_sublist C where A.devtype = B.devtype and A.devtype = C.devtype and A.scriptid = B.scriptid and A.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용')")

		#mapScriptPerScenarioAndMethodLine = self.makeMapScriptPerScenarioAndMethodLineFromOldDB()
		strjson = json.dumps(self.listmapcript, ensure_ascii=False)

		neolib.StrToFile(strjson, 'rsc/mapScriptPerScenarioAndMethodLine.json')







		return


class MakeDataValueTable(BaseTableInput):
	dsttable = "data_value_table"
	prefix = "dvt"
	colline = "scl_uid, pdt_uid, value, param, param_ext,comment"

	def processInserValues(self):
		listscl = self.dstdbHD.select("SELECT seq, scl_uid, sce_uid, `index`, method, title, param, param_ext, pck_uid, updt_date, reg_date, comment FROM adts.scenario_line where pck_uid != '';")
		listpacketData = self.dstdbHD.selectToMap("name","SELECT seq, pdt_uid, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment FROM adts.packet_data_type;")

		for row in listscl:
			param = row['comment']
			scl_uid = row['scl_uid']
			mapdddd = json.loads(param,object_pairs_hook=collections.OrderedDict)
			print(param)
			print(mapdddd)
			print()
			for key,value in mapdddd.items():
				param = ''
				pdt_uid = listpacketData[key]['pdt_uid']
				if value in ['EMPTY','REMOVE']:
					param = value
					value = ''
				self.appendLine(scl_uid=scl_uid, pdt_uid=pdt_uid, value=value, param=param,comment = key)

			#$print(mapdddd)

		None




class MakeScenarioDBFromOldDB(BaseMySQLRunnable):

	def init(self):
		list = ['STC.A.001.0z', 'STC.A.002.zz', 'STC.A.003.00', 'STC.A.004.00', 'STC.A.005.00', 'STC.A.006.0z',
				'STC.A.007.0z', 'STC.A.008.00', 'STC.A.009.00', 'STC.A.010.00', 'STC.A.014.zz', 'STC.A.015.00',
				'STC.A.016.00', 'STC.A.017.00', 'STC.A.018.00', 'STC.A.019.00', 'STC.A.020.00', 'STC.A.021.00',
				'STC.A.024.0z', 'STC.A.201.zz', 'STC.A.202.zz', 'STC.A.501.0z', 'STC.A.502.0z', 'STC.A.503.00',
				'STC.A.504.00', 'STC.A.505.00', 'STC.A.506.0z', 'STC.A.507.0z', 'STC.A.508.00', 'STC.A.509.00',
				'STC.A.510.00', 'STC.A.601.00', 'STC.A.602.00', 'STC.A.603.0z', 'STC.A.604.0z', 'STC.A.605.0z',
				'STC.A.606.0z', 'STC.A.607.0z', 'STC.A.608.0z', 'STC.A.609.00', 'STC.A.610.00', 'STC.A.611.00',
				'STC.A.612.00', 'STC.A.613.00', 'STC.A.614.00', 'STC.A.701.00', 'STC.A.702.00', 'STC.B.001.0z',
				'STC.B.002.0z', 'STC.B.003.00', 'STC.B.004.00', 'STC.B.005.00', 'STC.B.006.0z', 'STC.B.007.0z',
				'STC.B.008.00', 'STC.B.009.00', 'STC.B.010.00', 'STC.B.011.00', 'STC.B.012.00', 'STC.B.013.00',
				'STC.B.014.00', 'STC.B.015.00', 'STC.B.016.00', 'STC.B.017.00', 'STC.B.018.00', 'STC.B.501.0z',
				'STC.B.502.0z', 'STC.B.503.00', 'STC.B.504.00', 'STC.B.505.00', 'STC.B.506.0z', 'STC.B.507.0z',
				'STC.B.508.00', 'STC.B.509.00', 'STC.B.510.00', 'STC.B.701.00', 'STC.B.702.00', 'STC.D.001.00',
				'STC.D.002.00', 'STC.D.003.00', 'STC.D.004.00', 'STC.D.005.00', 'STC.D.006.00', 'STC.D.501.00',
				'STC.D.502.00', 'STC.D.503.00', 'STC.D.504.00', 'STC.D.505.00', 'STC.D.601.00', 'STC.D.701.00',
				'STC.D.702.00']
		listwithzero = []
		for tmp in list:
			str = tmp.replace('z', '0')
			listwithzero.append("'{0}'".format(str))

		strarrayform = ",".join(listwithzero)


	def makeMapCmdFromInputSrc(self):
		mapret = {}
		strmenu = neolib.StrFromFile('rsc/cmdmappingTable.txt')
		mapobj = map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
		listmenu = list(filter(lambda x: len(x)>4, mapobj))
		for cond,inst,newinst,title,param,param_ext,input_value in listmenu:
			mapret[inst] = cond,newinst,title,param,param_ext,input_value
		return mapret

	def ConvertValue(self,value,mapRows,input_value):
		arrayparam = json.loads(input_value)
		newarrayparam = []
		for tmp in arrayparam:
			newarrayparam.append(mapRows[tmp])


		return  value.format(* newarrayparam)

	def makeMapScriptPerScenarioAndMethodLineFromOldDB(self):
		lastseq = self.dstdbHD.lastSeq( 'scenario')
		lastseq += 1

		mapret = self.makeMapCmdFromInputSrc()
		self.listmapcript = self.select(
			"SELECT A.scriptid, instruction, delay, protocol, sentence, etc, direction,B.caseid,B.objective,A.devtype,B.profilename,C.description FROM test_smartro.script_maininfo A,test_smartro.script_sublist B,test_smartro.profile_profile_sublist C where A.devtype = B.devtype and A.devtype = C.devtype and A.scriptid = B.scriptid and A.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용')")

		self.listmapcriptsub = self.select(
			"SELECT B.scriptid, title, script, objective, category, subcategory, caseid, testcase, B.profilename,  C.description "
			"FROM test_smartro.script_sublist B,test_smartro.profile_profile_sublist C where B.devtype = C.devtype and B.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용');")

		listmapmethodline = self.dstdbHD.select(
										   "SELECT seq, pck_uid, name, type, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment FROM adts.packet;")

		mapmapmethodline = {}
		for maprow in listmapmethodline:
			mapmapmethodline[maprow['name']] = maprow


		for tmprow in self.listmapcriptsub:
			# print(tmprow['scriptid'],tmprow['title'],tmprow['caseid'])
			None

		prevscriptid = ''
		curuid = ''

		mapScriptPerScenarioAndMethodLine = {}

		for tmprow in self.listmapcript:
			pck_uid = ''
			instruction = tmprow['instruction']
			scriptid = tmprow['scriptid']
			profilename = tmprow['profilename']
			objective = tmprow['objective']
			description = tmprow['description']
			protocol = tmprow['protocol']
			if scriptid != prevscriptid:
				mapScriptPerScenarioAndMethodLine[scriptid] = {}

				mapScriptPerScenarioAndMethodLine[scriptid]['scenario'] = (
				scriptid, description, '', '', 'smatro_sc.py',
				'SMARTRO_SC',profilename,objective)  # ( 'name', 'discription', 'profile_sc', 'profile_reset_sc', 'script_file', 'classname')
				mapScriptPerScenarioAndMethodLine[scriptid]['method_line'] = []

			arrayMethodLine = mapScriptPerScenarioAndMethodLine[scriptid]['method_line']

			prevscriptid = scriptid
			if instruction not in mapret: continue

			cond, newinst, title, param, param_ext, input_value = mapret[instruction]
			title = self.ConvertValue(title, tmprow, input_value)
			param = self.ConvertValue(param, tmprow, input_value)

			if "전문" in instruction:
				map = self.ConvertFromSentence({}, param)[0]
				param = json.dumps(map, ensure_ascii=False)

				if "수신" in instruction:
					packetname = protocol+" 수신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']
					arrayMethodLine.append(('RECV', '수신', '$PORT00', '',''));
					arrayMethodLine.append(('CONFIRM_PACKET', title, param, '',pck_uid));
					#self.appendA('RECV', '수신', '$PORT00')
					#self.appendA('CONFIRM_PACKET', title, param, '{"TYPE":"MAIN","PAKCET":"%s"}' % tmprow['protocol'])

					None
				elif "송신" in instruction:
					packetname = protocol + " 송신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']

					arrayMethodLine.append(('MAKE_PACKET', title, param, '',pck_uid));
					arrayMethodLine.append(('SEND', '송신', '$PORT00', '',''));
					#self.appendA('MAKE_PACKET', title, param, '{"TYPE":"MAIN","PAKCET":"%s"}' % tmprow['protocol'])
					#self.appendA('SEND', '송신', '$PORT00')
					None

				continue
			arrayMethodLine.append( (newinst, title, param,'',''));
			#self.appendA(newinst, title, param)
		#self.appendA("================================================")


		return  mapScriptPerScenarioAndMethodLine


	def makeJsonFile(self):
		mapScriptPerScenarioAndMethodLine = self.makeMapScriptPerScenarioAndMethodLineFromOldDB()
		strjson = json.dumps(mapScriptPerScenarioAndMethodLine, ensure_ascii=False)

		neolib.StrToFile(strjson, 'rsc/mapScriptPerScenarioAndMethodLine.json')

	def deleteScenarioAndMethodLine(self):
		self.dstdbHD.select("DELETE FROM scenario ;DELETE FROM method_line")


	def InsertScenarioAndMethodLine(self,mapScriptPerScenarioAndMethodLine):

		lastseq = self.dstdbHD.lastSeq( 'scenario')
		lastseq += 1

		lastseqMethodLine = self.dstdbHD.lastSeq('method_line')
		lastseqMethodLine += 1

		sqldstfmt = "INSERT INTO scenario(   seq  ,sce_uid  ,scg_uid  ,name  ,discription  ,profile_sc  ,profile_reset_sc  ,script_file  ,classname  ,updt_date  ,reg_date  ,comment) " \
					"VALUES (%d  ,'%s','%s','%s','%s','%s','%s','%s','%s',now(),now(),'%s')"

		sqldstfmtMethodLine = "INSERT INTO method_line(" \
							  " seq  ,mtd_uid  ,sce_uid  ,`index`  ,method  ,title  ,param  ,param_ext ,pck_uid ,updt_date  ,reg_date  ,comment )" \
							  "VALUES (%d,'%s','%s',%d,'%s','%s','%s','%s','%s',now(),now(),'%s')"




		for scriptid, values in mapScriptPerScenarioAndMethodLine.items():
			scriptid, description, profile_sc, profile_reset_sc, script_file, classname, profilename, objective = \
			values['scenario']

			self.appendA("================================================")
			self.appendA("================================================")
			self.appendA("시나리오명", scriptid)
			self.appendA("사용프로파일", profilename)
			self.appendA("사전세팅", description)
			self.appendA("목적", objective)
			self.appendA("================================================")
			self.appendA('CMD', 'TITLE', 'PARAM', 'PARAM_EXT')
			self.appendA("================================================")

			curuid = 'sce_' + str(lastseq)
			objective = objective.replace("'", "\\'")
			sql = sqldstfmt % (
				lastseq, curuid, '', scriptid, objective, '', '', 'smatro_sc.py', 'SMARTRO_SC', '')
			print(sql)
			lastseq += 1
			self.dstdbHD.excute( sql)

			index = 0
			for method, title, param, param_ext,pck_uid in values['method_line']:
				self.appendA(method, title, param, param_ext)
				curuidMethodLine = 'mtd_' + str(lastseqMethodLine)
				param = param.replace("'", "\\'")
				param_ext = param_ext.replace("'", "\\'")
				sql = sqldstfmtMethodLine % (
					lastseqMethodLine, curuidMethodLine, curuid, index, method, title, param, param_ext,pck_uid, '')

				print(sql)
				self.dstdbHD.excute(sql)
				# seq  ,mtd_uid  ,sce_uid  ,`index`  ,method  ,title  ,param  ,param_ext  ,updt_date  ,reg_date  ,comment
				index += 1
				lastseqMethodLine += 1

			self.appendA("================================================")


	def mainProcess(self):

		self.deleteScenarioAndMethodLine()
		#return


		self.makeJsonFile()
		strjson = neolib.StrFromFile('rsc/mapScriptPerScenarioAndMethodLine.json')
		mapScriptPerScenarioAndMethodLine = json.loads(strjson);

		self.InsertScenarioAndMethodLine(mapScriptPerScenarioAndMethodLine)


class BASE_PACKET_PROCESS:

	listMap = {}
	resultBuff = ""#hex str output

	def initStart(self):
		None

	def initLoop(self,mapvalue):
		None
	def doUnit(self,mapvalue):
		None

	def endLoop(self, mapvalue):
		None

	def Run(self):
		self.initRun()

		for mapvalue in self.listMap:
			self.initLoop(mapvalue)
			self.doUnit(mapvalue)
			self.endLoop(mapvalue);
		self.endLoop()






"""
이 클래스는 프로파일 세팅을 시나리오로 만드는 클래스 이다.
"""
class MakeProfileToScenario(MakeScenarioDBFromOldDB):
	def makeMapScriptPerScenarioAndMethodLineFromOldDB(self):
		lastseq = self.dstdbHD.lastSeq( 'scenario')
		lastseq += 1


		listmap = self.olddbHD.select(
			"SELECT seq, uid, profilename, description, devtype FROM test_smartro.profile_profile_sublist where devtype = 'V100_EN07';")

		prevscriptid = ''
		curuid = ''

		mapScriptPerScenarioAndMethodLine = {}

		for tmprow in listmap:
			profilename = tmprow['profilename']
			description = tmprow['description']

			mapScriptPerScenarioAndMethodLine[profilename] = {}

			mapScriptPerScenarioAndMethodLine[profilename]['scenario'] = (
				profilename, description, '', '', 'smatro_sc.py',
				'SMARTRO_SC', profilename,
				description)  # ( 'name', 'discription', 'profile_sc', 'profile_reset_sc', 'script_file', 'classname')
			mapScriptPerScenarioAndMethodLine[profilename]['method_line'] = []

			arrayMethodLine = mapScriptPerScenarioAndMethodLine[profilename]['method_line']


		# self.appendA(newinst, title, param)
		# self.appendA("================================================")


		return mapScriptPerScenarioAndMethodLine

	def mainProcess(self):
		mapScriptPerScenarioAndMethodLine = self.makeMapScriptPerScenarioAndMethodLineFromOldDB();


		self.InsertScenarioAndMethodLine(mapScriptPerScenarioAndMethodLine)


		None



#MakeScriptSentenceFromMySQL().Run()
#MakeScriptSentenceFromMySQL().Run()
#countProfileFromMySQL().Run()
#checkInitProfilecountProfileFromMySQL().Run()
#adjustProfileConfigFromMySQL().Run()
#ProfileSettings().Run()


#MakePacketDateType(False).Run()
#MakePacket(False).Run()
#MakePacketDataUnit().Run(False)

#MakeScenario().Run()
MakeScenarioLine().Run(False)
MakeDataValueTable().Run(False)
#MakeScenarioDBFromOldDB().Run()
#MakeProfileToScenario().Run()


exit()