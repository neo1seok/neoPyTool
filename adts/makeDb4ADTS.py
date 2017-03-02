import collections
import os
import re
import  shutil
import time

import pymysql
import  simplejson as json

import neolib.neolib as neolib
import neolib.neolib4Win as neolib4Win
import xlrd

from  neolib.db import dbHandleing
from  neolib.db import MakeDataFieldsClass


class BaseMySQLRunnable(neolib4Win.NeoAnalyzeClasss):
	ignorenames = ['Message Type', '거래구분코드']



	def setDefArges(self):
		super(BaseMySQLRunnable, self).setDefArges()
		self.defMapArgs.update({'dbaddress': 'localhost'})

	def test(self,**kwargs):
		for key,value in kwargs.items():
			print(key,value)
		None

	def test2(self,**kwargs):
		self.test(**kwargs)
		None

	def InitRun(self):

		# self.test2(aaa='1',aaa2='2')

		self.dbaddress = self.mapArgs['dbaddress']
		self.listmap = []


		print("dst db:"+self.dbaddress)
		self.olddbHD = dbHandleing(host='localhost', port=3306, user='neo1seok', passwd='tofhdna1pi',db='test_smartro', charset='utf8')
		self.dstdbHD = dbHandleing(host=self.dbaddress, port=3306, user='ictk', passwd='#ictk1234',	  db='adts', charset='utf8')
		#self.dstdbHD = dbHandleing(host='localhost', port=3306, user='ictk', passwd='#ictk1234', db='adts',	   charset='utf8')
		self.strlines = ""

		None


	def endRun(self):
		# fb = open('out.txt', 'wb')
		# fb.write(self.strlines.encode())
		# fb.close()
		#
		# neolib4Win.SetClipBoard(self.strlines)

		self.olddbHD.conn.close()
		self.dstdbHD.conn.close()
		neolib.NeoRunnableClasss.endRun(self)


	def makeMapMapDBFromListMapDB(self,key,listMapDB):
		return dbHandleing.makeMapMapDBFromListMapDB(key,listMapDB)



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
	dispalaytitle ="시나리오 상태"
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


	def setDefArges(self):
		super(BaseTableInput, self).setDefArges()
		self.defMapArgs.update({'deleteTable': True})

	def doRun(self):
		self.strlines = ""

		self.makeMap4Protocol()
		self.makeMap4Type()

		if self.mapArgs['deleteTable'] :
			self.deleteTable()





		self.cols = re.split(r',\s*',self.colline)
		self.listmap = []


		self.processInserValues()

		for row in self.listmap:
			print(row)

		self.processInserToDB()

		self.processAfterDB()

		time.sleep(0.3)




		None


	def makeMapCmdFromTxt(self,strtxt):

		strmenu = neolib.StrFromFile(strtxt)
		mapobj = map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
		return mapobj
	def deleteTable(self):
		self.dstdbHD.deleteTable(self.dsttable)

	def processInserValues(self):
		None

	def processInserToDB(self):
		lastseq = self.dstdbHD.lastSeq(self.dsttable)
		self.dstdbHD.insertList(self.dsttable, self.prefix, self.listmap, lastseq)

	def processAfterDB(self):
		None

	def getOptions(self, types, defoption = ""):

		if 'F' not in types:
			if 'SI' not in types:
				return "FS"
			# self.appendLine(name="FS", length="1", encoding='HEX', value="1C",param=strparam,)
			strscript = 'CALCL_ENGTH'

		if 'SI' in types:
			return "SI"

		return defoption

class MakeEnvSelection(BaseTableInput):
	dsttable = "env_selection"
	colline = "name,discription"
	prefix = "esl"

	def processInserValues(self):
		self.appendLine(name='V100_EN07', discription='스마트로 V100_EN07 단말기 테스트 ')
		self.appendLine(name='V100_EN09', discription='스마트로 V100_EN09 단말기 테스트 ')

		None


class MakeEnvSetting(BaseTableInput):
	dsttable = "env_setting"
	colline = "esl_uid,item, value,comment"
	prefix = "ens"

	def processInserValues(self):
		eslmaps = self.dstdbHD.select("""
SELECT seq, esl_uid, name, discription, updt_date, reg_date, comment
FROM env_selection;
		""")

		for maps in eslmaps:
			name = maps['name']
			esl_uid = maps['esl_uid']

			self.InsertEnvSetting(name,esl_uid)

			None





		None
	def InsertEnvSetting(self,name,esl_uid):

		mapEnv = collections.OrderedDict([
			("DEVICE_TYPE", name),
			("DEVICE_MODEL", "T224"),
			("CHANNEL_MAIN", "chn_2"),
			("CHANNEL_DONGLE", "chn_2"),
			("CHANNEL_POS", "chn_3"),
			("CRYPTO_CNF_PATH", 'C:/TMP/SMARTRO/INISAFESem.cnf'),
			("SIGNPADE_PATH", 'D:/PROJECT/toolrnd/DeviceTesterSystem/script/smt_signpad.dll'),

		])

		if self.dbaddress == "192.168.0.75":
			mapEnv[
				"CRYPTO_CNF_PATH"] = 'E:/SMARTRO/ETC_Projects/toolrnd/DeviceTesterSystem/ISEM_Files/conf/INISAFESem.cnf'
			mapEnv["SIGNPADE_PATH"] = 'E:/SMARTRO/ETC_Projects/toolrnd/DeviceTesterSystem/script/smt_signpad.dll'

		mapdefvalue = self.olddbHD.select(
			"SELECT profileid, value FROM profile_config_maininfo where devtype = '%s';"%name)

		mapdefvaluesce = self.olddbHD.select(
			"""
			SELECT instruction, scenario, optionscenario, devtype
FROM test_smartro.maindev_scenario where keypadtype = 'T224' and devtype = 'V100_EN07';
			""")

		for row in mapdefvalue:
			profileid = row['profileid']
			value = row['value']

			mapEnv[profileid] = value

		for key, val in mapEnv.items():
			self.appendLine(item=key, value=val,esl_uid=esl_uid)

		for row in mapdefvaluesce:
			instruction = row['instruction']
			scenario = row['scenario']
			optionscenario = row['optionscenario']
			self.appendLine(item=instruction, value=scenario, esl_uid=esl_uid,comment =optionscenario )




class MakeChannel(BaseTableInput):
	dsttable = "channel"
	colline = "type, discription, param, classname"
	prefix = "chn"
	def processInserValues(self):
		mapEnv =[
			('UART 0',"UART", json.dumps({"PORTNAME":"COM4","BAUDRATE":38400}, ensure_ascii=False)),
			('TCP 1',"TCPSERVER", json.dumps({"PORT":5510}, ensure_ascii=False)),
			('UART 2', "UART", json.dumps({"PORTNAME":"//.//COM09","BAUDRATE":38400}, ensure_ascii=False)),
			('TCP 2', "TCPSERVER", json.dumps({"PORT":8056},ensure_ascii=False)),
		]



		for name,type,param in mapEnv:
			self.appendLine(name=name,type = type,param= param)


		None
class MakePacketDateType(BaseTableInput):
	dsttable = "packet_data_type"
	colline = "name, length, variation, value_encoding, char_range, fixed_value, option, make_param,confirm_param"
	prefix = "pdt"

	def processInserValues(self):

		self.appendLine(name="STX", length="1", value_encoding='HEX', fixed_value="02")
		self.appendLine(name="ETX", length="1", value_encoding='HEX', fixed_value="03")
		self.appendLine(name="CRC", length="4", value_encoding='ASCII',make_param=json.dumps({'variable':'value','method':'CRC','order':'2'}),confirm_param="")

		for key, value in self.mapOldDBMainType.items():
			self.index = 0
			self.processDataTypes('',value)


		self.appendLine(name="CRC_STMS", length="7", value_encoding='ASCII',
						make_param=json.dumps({'variable': 'value', 'method': 'CRC_STMS', 'order': '2'}), confirm_param="")

		self.appendLine(name="전문길이_STMS", length="4", value_encoding='ASCII',
						make_param="",confirm_param="")



		None
	def getStrMap(self,map):
		strparam = ''
		if len(map) > 0:
			strparam = json.dumps(map, ensure_ascii=False)
		return strparam


	def processDataTypes(self, servicecode,datamap):
		name = datamap['name']
		length = datamap['length']
		options = datamap['options']
		chartype = datamap['chartype']

		types = options.split('|')
		strv = ''

		mapparam = collections.OrderedDict()
		mapMakeParam = collections.OrderedDict()
		mapConfirmParam = collections.OrderedDict()

		if 'V' in types:
			strv = 'TRUE'
			mapConfirmParam['variable'] = 'length'
			mapConfirmParam['method']='CALC_LENGTH'

		order = '0'
		value = ''
		if name == '전문길이':
			order = '1'
			mapMakeParam["order"] = '1'
			mapMakeParam['variable'] = 'value'
			mapMakeParam['method'] = "MAKE_LENGTH"


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
		retoption = self.getOptions(types, "")
		if retoption != '':
			mapparam["START_TAG"] = self.getOptions(types,"")

		# if 'F' not in types:
		# 	if 'SI' not in types:
		# 		mapparam["START_TAG"] = "FS"
		# 		#self.appendLine(name="FS", length="1", encoding='HEX', value="1C",param=strparam,)
		# 	strscript = 'CALCL_ENGTH'
		#
		# if 'SI' in types:
		# 	mapparam["START_TAG"] = "SI"
		# 	#self.appendLine(name="SI", length="1", encoding='HEX', value="0F",param=strparam,)

		strMakeparam = self.getStrMap(mapMakeParam)
		strConfirmparam = self.getStrMap(mapConfirmParam)

		strparam = self.getStrMap(mapparam)


		self.appendLine(name=name, length=length, variation=strv, value_encoding='ASCII', char_range=chartype, fixed_value=value,
						option=strparam, make_param=strMakeparam,confirm_param=strConfirmparam)


class MakePacket(BaseTableInput):
	dsttable = "packet";
	prefix = "pck"
	colline = "name, type, discription,  packet_class"
	def makePacketName(self,protocol,direction):
		tail = '수신' if direction == 'D2A'  else '송신'

		return protocol + " " + tail;

	def processInserValues(self):
		for key, value in self.mapOldDBMainProtocol.items():
			protocol = value['protocol']
			direction = value['direction']
			name = self.makePacketName(protocol,direction)

			if name in ["STMS/ALIVE 수신", "STMS/ALIVE 송신"]:
				self.appendLine(name=name, type="MAIN", packet_class="PACKET_MAIN_STMSALIVE")
				continue




			self.appendLine(name=name,type="MAIN",packet_class="PACKET_MAIN")

		None

class MakePacketDataUnit(MakePacket):
	dsttable = "packet_data_unit";
	colline = "pck_uid, index, pdt_uid, def_value,comment"
	prefix = "pdu"

	def processInserValues(self):
		#make_class, confirm_class
		mapPacket = self.dstdbHD.selectToMap("name","SELECT seq, pck_uid, name, type, discription,  packet_class FROM adts.packet;")
		self.mapType = self.dstdbHD.selectToMap("name", "SELECT seq, pdt_uid, name, length, variation, value_encoding, char_range, fixed_value,  updt_date, reg_date, comment FROM adts.packet_data_type;")

		print([ key for key,value in self.mapType.items()])
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
				if packetName.startswith('STMS'):
					if typename == '전문길이':
						typename = typename+'_STMS'





				self.appendSel(pck_uid, typename,value)

			self.appendSel(pck_uid, 'ETX')
			if not packetName.startswith('STMS'):
				self.appendSel(pck_uid, 'CRC')
			else:
				self.appendSel(pck_uid, 'CRC_STMS' )



		None

	def appendSel(self,pck_uid,typename,defvalue=''):
	#	print(typename)
	#	print( self.mapType[typename])

		pdt_uid = self.mapType[typename]['pdt_uid']
		self.appendLine(pck_uid=pck_uid, index=self.index, pdt_uid=pdt_uid, def_value=defvalue,comment=typename)
		self.index += 1






#이 클래스는 스마트로의 스크립트 정보를 이용하여
#새로운 커맨드 라인을 만드는 클래스이다.
#adts/cmdmappingTable.txt 에 instruction mapping 정보가
#뉴라인 탭 형태의 테이블 정보로 들어 있다.

class MakeScenario(BaseTableInput):
	dsttable = "scenario"
	prefix = "sce"
	colline = "scg_uid, name, discription, param, param_ext, type, classname,comment"

	def processInserValues(self):
		listmapcriptsub = self.olddbHD.selectToMap('scriptid',
			"SELECT B.scriptid, title, script, objective, category, subcategory, caseid, testcase, B.profilename,  C.description "
			"FROM script_sublist B,profile_profile_sublist C where B.devtype = C.devtype and B.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용');")

		mapScenario = self.dstdbHD.selectToMap('name',
											   "SELECT * FROM adts.scenario where type = 'profile';")

		for key,row in listmapcriptsub.items():
			objective = row['objective']
			title = row['title']
			profilename = row['profilename']

			sce_uid = mapScenario[profilename]['sce_uid'];
			sce_uid_reset = mapScenario[profilename + " RESET"]['sce_uid'];
			discription = title if title != '' else objective

			param_ext = json.dumps({"sce_uid_profile": sce_uid, "sce_uid_profile_reset": sce_uid_reset})

			self.appendLine(name=key,discription=discription,classname='SMARTRO_SC',param_ext=param_ext)



		None

class MakeScenarioLine(BaseTableInput):
	dsttable = "scenario_line"
	prefix = "scl"
	#colline = "sce_uid, index, method, title, param, param_ext, pck_uid,comment"
	colline = "sce_uid, index, method, title, param, param_ext,pck_uid, comment"

	def makeMapJustValue(self, result_list):
		mapresultvalus = collections.OrderedDict()
		for id, VFT, value in result_list:
			strid = str(int(id))
			name = self.mapOldDBMainType[strid]['name']


			sepoptions = self.mapOldDBMainType[strid]['options'].split('|')

			if name in self.ignorenames:
				continue

			retoption = self.getOptions(sepoptions)



			if VFT == 'T':
				value = 'EMPTY' if 'O' not in sepoptions else 'REMOVE'
				if value == 'EMPTY':
					if retoption == "FS" :
						value = ''
					else :
						value = 'REMOVE'



			mapresultvalus[name] = value

			None

		return mapresultvalus


	def ConvertFromSentence(self,mapresultvalus,sentence):

		result_list = re.findall(self.sentencepatt, sentence)

		remove = re.sub(self.sentencepatt, "", sentence)

		for k,v in self.makeMapJustValue(result_list).items():
			mapresultvalus[k] = v;
		return (mapresultvalus,remove)


	def processInserValues(self):

		#self.makeJsonFile()
		strjson = neolib.StrFromFile('adts/mapScriptPerScenarioAndMethodLine.json')
		self.listmapcript = json.loads(strjson);

		mapdstScenario = self.dstdbHD.selectToMap('name',"SELECT * FROM adts.scenario;")
		mapmapmethodline = self.dstdbHD.selectToMap('name',"SELECT seq, pck_uid, name, type, discription,  packet_class, updt_date, reg_date, comment FROM adts.packet;")


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
			prevsce_uid = ""
			if instruction == '숫자':
				None

			if prevscriptid in mapdstScenario:
				prevsce_uid = mapdstScenario[prevscriptid]['sce_uid']

			if scriptid != prevscriptid:
				if prevsce_uid  != "":
					self.appendLine(sce_uid=prevsce_uid, index=index, method='PRINT_TITLE', title=self.dispalaytitle, param='주 동작 종료')

				index = 0
				self.appendLine(sce_uid=sce_uid, index=index, method='PRINT_TITLE', title=self.dispalaytitle,param = '주 동작 시작')
				index += 1




			prevscriptid = scriptid
			if instruction not in mapret: continue

			cond, newinst, title, param, param_ext, input_value = mapret[instruction]

			title = self.ConvertValue(title, tmprow, input_value)
			param = self.ConvertValue(param, tmprow, input_value)

			if param_ext == 'N': param_ext =''

			if "전문" in instruction:
				map = self.ConvertFromSentence(collections.OrderedDict(), param)[0]
				param = json.dumps(map, ensure_ascii=False)


				if "수신" in instruction:
					packetname = protocol + " 수신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']
					param_ext = "{'pck_uid':'%s'}" % pck_uid
					param_ext = param_ext.replace("'","\"")
					param_ext = ''

					self.appendLine(sce_uid=sce_uid, index=index, method ='RECV' ,title='수신', param="$MAP_ENV['CHANNEL_MAIN']")
					index+=1
					self.appendLine(sce_uid=sce_uid, index=index, method='CONFIRM_PACKET', title=title, param=packetname ,param_ext=param_ext,pck_uid = pck_uid,comment= param )
					None

				elif "송신" in instruction:
					packetname = protocol + " 송신"
					pck_uid = mapmapmethodline[packetname]['pck_uid']
					param_ext = "{'pck_uid':'%s'}" % pck_uid
					param_ext = param_ext.replace("'", "\"")
					param_ext = ''

					self.appendLine(sce_uid=sce_uid, index=index, method='MAKE_PACKET', title=title, param=packetname ,param_ext=param_ext,pck_uid = pck_uid,comment=param)
					index += 1
					self.appendLine(sce_uid=sce_uid, index=index, method='SEND', title='송신', param="$MAP_ENV['CHANNEL_MAIN']")
					None
				index += 1
				continue
			if newinst == "INPUT_DIRECT, CALL_SCENARIO":
				None
			self.appendLine(sce_uid=sce_uid,method=newinst,index=index,title=title,param=param,param_ext=param_ext	)
			index+=1


		self.appendLine(sce_uid=sce_uid, index=index, method='PRINT_TITLE', title=self.dispalaytitle,
							param='주 동작 종료')

	def processInserToDBa(self):
		lastseq = self.dstdbHD.lastSeq(self.dsttable)
		for tmp in self.listmap:
			self.dstdbHD.insert(self.dsttable, self.prefix, tmp, lastseq)
			lastseq+=1



		None





	def makeMapCmdFromInputSrc(self):
		mapret = {}
		#strmenu = neolib.StrFromFile('adts/cmdmappingTable.txt')
		mapobj =self. makeMapCmdFromTxt('adts/cmdmappingTable.txt')
		#map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
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

		neolib.StrToFile(strjson, 'adts/mapScriptPerScenarioAndMethodLine.json')







		return

class MakeScenarioGroup(BaseTableInput):
	dsttable = "scenario_group"
	prefix = "scg"
	colline = "scg_uid_parent, name, discription,comment"

	def processInserValues(self):
		patter = r'([A-Z]{3}\.[A-Z]{1})\.\d{3}\.\d{2}'

		mapSubScript = self.olddbHD.selectToMap('scriptid',
		"""
		SELECT seq, uid, scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype
		FROM test_smartro.script_sublist where devtype = 'V100_EN07';
		""" )

		listdistict = self.olddbHD.select("SELECT distinct category		FROM test_smartro.script_sublist where devtype = 'V100_EN07';")

		mapScenario = self.dstdbHD.select( "SELECT * FROM adts.scenario where type != 'profile';")
		seq = 1;
		mapcategory = {}
		for rows in listdistict:
			category = rows['category']
			mapcategory[category] = 'scg_'+str(seq)
			category = re.sub(r'\d{2}\.(.+)', r'\1', category)
			self.appendLine(name=category)
			seq+=1

		self.mapADD = {}
		for row in mapScenario:
			key = row['name']
			sce_uid = row['sce_uid']
			subcategory= mapSubScript[key]['subcategory']
			subcategory = re.sub(r'\d{2}\.\d{2}\.(.+)',r'\1',subcategory)
			category = mapSubScript[key]['category']
			testcase = mapSubScript[key]['testcase']

			name = re.sub(patter,r'\1',key)
			if name not in self.mapADD:

				scg_uid_parent = mapcategory[category]
				self.appendLine(scg_uid_parent=scg_uid_parent,name=subcategory, discription=testcase,comment=name)
				self.mapADD[name] = ('scg_'+str(seq), [])
				seq += 1

			self.mapADD[name][1].append(sce_uid)

			None
		#	self.appendLine(name=key,discription="")



		None

	def processAfterDB(self):

		for key,values in self.mapADD.items():
			scg_uid, uids =values
			for uid in uids:
				sql = "UPDATE adts.scenario SET  scg_uid = '%s' WHERE sce_uid = '%s'"%(scg_uid,uid)
				print(sql)
				self.dstdbHD.excute(sql)
			None






		None
class MakeScenarioEtc(BaseTableInput):
	dsttable = "scenario"
	prefix = "sce"
	colline = "scg_uid, name, discription,  classname,comment"

	def processInserValues(self):
		retdb = self.dstdbHD.select(
			"SELECT seq, sce_uid, scg_uid, name, discription, classname, type, updt_date, reg_date, comment FROM adts.scenario where name = 'DEVTEST';")
		if len(retdb) >0 : return
		self.appendLine(name='DEVTEST', scg_uid='scg_1',discription='단말 접속 설정', classname='SMARTRO_SC' )


class MakeScenarioLineEtc(BaseTableInput):
	dsttable = "scenario_line"
	prefix = "scl"
	colline = "sce_uid, index, method, title, param, param_ext, comment"

	def processInserValues(self):
		retdb = self.dstdbHD.select("SELECT seq, sce_uid, scg_uid, name, discription, classname, type, updt_date, reg_date, comment FROM adts.scenario where name = 'DEVTEST';")
		retmap = retdb[0]
		sce_uid = retmap['sce_uid']
		index = 0
		self.appendLine(sce_uid=sce_uid, index=index, method='PRINT_TITLE', title=self.dispalaytitle,param = '주 동작 시작')
		index+=1

		self.appendLine(sce_uid=sce_uid, method="DEVTEST", index=index, title="신호대기중",param="$MAP_ENV['CHANNEL_MAIN']")
		index += 1

		self.appendLine(sce_uid=sce_uid, index=index, method='PRINT_TITLE', title=self.dispalaytitle,						param='주 동작 종료')
		index += 1





class MakeDataValueTable(BaseTableInput):
	dsttable = "data_value_table"
	prefix = "dvt"
	colline = "scl_uid, pdt_uid, value, param, param_ext,comment"

	def processInserValues(self):
		listscl = self.dstdbHD.select("SELECT * FROM adts.scenario_line where method in ('CONFIRM_PACKET','MAKE_PACKET');")
		listpacketData = self.dstdbHD.selectToMap("name","SELECT seq, pdt_uid, name, length, variation, value_encoding, char_range, fixed_value, option, updt_date, reg_date, comment FROM adts.packet_data_type;")

		for row in listscl:
			comment = row['comment']
			scl_uid = row['scl_uid']
			param = row['param']
			mapdddd = json.loads(comment,object_pairs_hook=collections.OrderedDict)

			mapLength = {}

			mapLength['makepacket_method'] = 'MakeProtocolLength'

			if param in ['STMS/ALIVE 수신','STMS/ALIVE 송신']:
				mapLength['makepacket_method'] = 'MakeProtocolLength_STMS'
				None

			#self.appendLine(scl_uid=scl_uid, pdt_uid='pdt_3', value=value, param_ext='', comment='CRC')
			#self.appendLine(scl_uid=scl_uid, pdt_uid='pdt_4', value=value, param_ext='',comment = '전문길이')


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


class MakeScenarioByProfile(MakeScenario):
	#/"scg_uid, name, discription, profile_sc, profile_reset_sc, script_file, classname"
	def processInserValues(self):
		mapobj = self.makeMapCmdFromTxt('adts/profile.txt')
		mapobj = list(filter(lambda x: x[0] != '' and x[0] != '이름', mapobj))

		#listProfileanme = self.olddbHD.select("SELECT seq, uid, profilename, description, devtype FROM test_smartro.profile_profile_sublist;")
		for row in mapobj :
			profileName = row[0];
			discription = row[1];

			self.appendLine(name=profileName,discription=discription,classname='SMARTRO_SC',type="profile" )
			self.appendLine(name=profileName+" RESET", discription=discription +" 기본값 복구", classname='SMARTRO_SC', type="profile")
		None



class MakeScenarioLineByProfile(MakeScenarioLine):
	patternFindRepeatEnd = r'((종료(,*\s*))+)'
	patternFindOptionMenu = r'(특수),\s(\d{4}),\s*(\d)'
	patternFindEnvMap = r'\{D:([가-힣A-Za-z0-9+]+)}'
	replaceFindEnvMap  = r"$MAP_ENV['\1']"

	def cbsub(self,matchobject):
		#print(matchobject.group(0))
		allstr = matchobject.group(0);
		repeatcount = len(re.findall("(종료)", allstr))



		return "\n종료(%d)\n"%repeatcount

	def processInputLien(self,strline):
		ret = []
		strline = re.sub(self.patternFindOptionMenu, r'\1|\2|\3\n', strline)
		strline = re.sub(self.patternFindRepeatEnd, self.cbsub, strline)
		strline = re.sub(self.patternFindEnvMap, r"\n$MAP_ENV['\1']\n", strline)
		strline = re.sub(r',[ ]*', "|", strline)
		strline = re.sub(r'(\n|^)\|', r"\1", strline)
		strline = re.sub(r'\|(\n|$)', r"\1", strline)
		strline = re.sub(r'(\n)입력', "|입력\n", strline)
		strline = re.sub(r'입력\|', "입력\n", strline)
		strline = re.sub(r'\n{2,5}', r"\n", strline)


		return strline
	def processInserValues(self):
		mapScenario = self.dstdbHD.selectToMap('name',"SELECT *  FROM adts.scenario where type = 'profile';")
		mapobj = self.makeMapCmdFromTxt('adts/profile.txt')
		mapobj = list(filter(lambda x:x[0] !='', mapobj))
		for tmp in mapobj:
			#print(tmp)
			profileName = tmp[0];
			if(profileName == "Terminal Profile 01") :continue
			if (profileName == "이름"): continue
			discription = tmp[1];
			setInput = tmp[2];
			resetInput = tmp[3]
			setInput = self.processInputLien(setInput)
			resetInput = self.processInputLien(resetInput)
			sce_uid = mapScenario[profileName]['sce_uid'];
			sce_uid_reset = mapScenario[profileName + " RESET"]['sce_uid'];

			# setInput = re.sub(r',\s*',"|",setInput)
			# resetInput = re.sub(r',\s*', "|",resetInput )
			# resetInput = re.sub(r'\{D:([가-힣A-Za-z0-9+]+)}', r"$MAP_ENV['\1']", resetInput)
			# resetInput = re.sub(r'((종료(\|*))+)', self.cbsub, resetInput)
			# setInput = re.sub(r'(((종료)(\|*))+)', self.cbsub, setInput)

			print("%s(%s)\nSET:%s\nRESET:%s\n"%(profileName,sce_uid,setInput,resetInput))
			index = 0

			self.appendLine(sce_uid=sce_uid, method="PRINT_TITLE", index=index, title=self.dispalaytitle, param='사전 설정 시작')
			index += 1

			for tmp in setInput.split('\n'):
				if tmp == '' : continue
				self.appendLine(sce_uid=sce_uid, method="INPUT_KEYPAD", index=index, title='키패드 입력', param=tmp)
				index += 1

			self.appendLine(sce_uid=sce_uid, method="PRINT_TITLE", index=index, title=self.dispalaytitle, param='사전 설정 종료')
			index += 1

			index = 0

			self.appendLine(sce_uid=sce_uid_reset, method="PRINT_TITLE", index=index, title=self.dispalaytitle, param='사전 재설정 시작')
			index += 1

			for tmp in resetInput.split('\n'):
				if tmp == '': continue
				self.appendLine(sce_uid=sce_uid_reset, method="INPUT_KEYPAD", index=index, title='키패드 입력', param=tmp)
				index += 1

			self.appendLine(sce_uid=sce_uid_reset, method="PRINT_TITLE", index=index, title=self.dispalaytitle, param='사전 재설정 종료')
			index += 1






		None


class MakeMainProcess(MakeScenarioLine):
	dsttable = "main_process"
	prefix = "mpr"
	colline = "scl_uid, pdt_uid, value, param, param_ext,comment"

	None
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

class DropAndCreateTable(BaseMySQLRunnable):
	def doRun(self):
		name = input("Are u sure for drop and create? yes or no ")

		if name != 'yes': return
		#
		# tables = re.split(r',\s',"channel, data_result, data_value_table, env_setting, main_process, packet, packet_data_type, packet_data_unit, scenario, scenario_group, scenario_line, test_result, test_info,test_env")
		# deleteSqlrArray = []
		# for tmp in tables:
		# 	#deleteSqlrArray.append("drop table  %s;\n"%tmp)
		# 	sql = "drop table  %s;\n" % tmp
		# 	try:
		# 		self.dstdbHD.excute(sql)
		# 		time.sleep(0.3)
		# 	except Exception as e:
		# 		print(e)
		#
		# # #sql = "".join(deleteSqlrArray)




		strtxt = neolib.StrFromFile('adts/DROP.SQL', enc='utf-8')
		tables = re.split(r';\s',  strtxt)
		deleteSqlrArray = []
		for tmp in tables:
			# deleteSqlrArray.append("drop table  %s;\n"%tmp)
			sql = tmp
			try:
				self.dstdbHD.excute(sql)
				time.sleep(0.3)
			except Exception as e:
				print(e)


		sql = neolib.StrFromFile('adts/TABLE.SQL',enc='utf-8')
		self.dstdbHD.excute(sql)
		time.sleep(0.3)

		None

class MakeNameFieldsClass(MakeDataFieldsClass):

	###mainfmt ="{0}\t{1}"
	mainfmt ='''<td valign="top">
<div style="margin: 25px;padding: 10px;border-radius: 10px;width:200px;height: auto;border:1px solid #000;color:white;background:#5b9bd5;">
<h4 style="margin: 1px">{0}</h4>
{1}
</div></td>'''
	#fieldfmt = "{0}"
	fieldfmt = '''{0}</br>'''

	sep = ""
	def doRun(self):

		ret = self.makeMapFromExcel(self.xlsDbFile)
		self.strlines  += '''<table width="300" height="200"  align="left" style='background-color:#f0fff0; filter: alpha(opacity=50); border:1 solid #009900; background-image :url(img/hobbang.gif);'>'''

		self.strlines += '''<tr>'''
		idx = 0
		for key, fields in ret.items():
			strarray = [self.fieldfmt.format(tmp[0]) for tmp in fields]
			islinesep = idx%3 == 0
			if islinesep :
				if islinesep: self.strlines += '''</tr>'''
				self.strlines += '''<tr>'''
			strline = self.mainfmt.format(key, self.sep.join(strarray))
			self.strlines += strline


			idx+=1
		if islinesep: self.strlines += '''</tr>'''
		self.strlines += ''' </table>'''

		neolib.StrToFile(self.strlines,"adts/tables.html")

		None
'''
이 클래스는
modulelist4ADTS.txt로 부터 모듈 구분, 프리픽스,모듈 이름 등을 얻어온후
TempLibrary란 프로젝트를 기반으로 그 밑에 파일 등을 변경하여
새로운 프로젝트를 생성 한다.
'''
class MakeCSharpProject(neolib.NeoRunnableClasss):
	orgname = "TempLibrary"
	basepath = "D:/PROJECT/자동단말기검수/SRC/DeviceTesterSystemAA"
	orgpath = basepath+"/"+orgname

	availext = ['.csproj','.cs']


	def getLists(self,orgpath):
		retarray = []
		for root, dirs, files in os.walk(self.orgpath):
			for basename in files:
				root = root.replace("\\", "/")
				if self.isFilter2Skip(root,basename): continue
				retarray.append((root,basename))
				#self.processFiles(root, basename)

		return retarray

	def CopyProject(self):

		for root,basename in self.arrayorgpath:
			relparentDir = root.replace(self.orgpath, "")
			dstdir = self.dstpath + "/" + relparentDir
			fullpath = root + "/" + basename

			if basename == self.orgname + ".csproj":
				basename = self.dstprojname + ".csproj"

			if basename == self.orgname + ".cs":
				basename = self.dstprojname + ".cs"

			dstfullpath = dstdir + "/" + basename

			neolib.MakeDir(dstdir)

			# print(ntpath.basename(fullpath))
			# print(ntpath.dirname(fullpath))


			print(fullpath, "\n", dstfullpath)
			shutil.copy(fullpath, dstfullpath)


		#for root, dirs, files in os.walk(self.orgpath):
		#	for basename in files:
	def ChangeContents(self):
		def changeFunction(contents):
			contents = contents.replace(self.orgname, self.dstprojname)
			return contents

		def changeAssemblyInfo(contents):
			contents = contents.replace(self.orgname, self.dstprojname)
			contents = re.sub(r'\[assembly:\s+Guid\("([\w\d-]+)"\)\]','[assembly: Guid("%s")]'%self.uuid,contents)
			return contents

		def changeCs(contents):
			contents = contents.replace("NameSpaceTempLibrary", "%s.%s"%(self.process,self.name) )
			contents = contents.replace("ClassTempLibrary", "%s : CommLib.BaseClass.Base%s"%(self.dstprojname,self.name))

			return contents
		self.changeContentsUnit("{0}/{1}.cs".format(self.dstpath, self.dstprojname),changeCs)
		self.changeContentsUnit("{0}/{1}.csproj".format(self.dstpath, self.dstprojname),changeFunction)
		self.changeContentsUnit("{0}/Properties/AssemblyInfo.cs".format(self.dstpath),changeAssemblyInfo)
		# maincs = neolib.StrFromFile("{0}/{1}.cs".format(self.dstpath,self.dstprojname))
		# maincsproj = neolib.StrFromFile("{0}/{1}.csproj".format(self.dstpath, self.dstprojname))
		# AssemblyInfo = neolib.StrFromFile("{0}/Properties/AssemblyInfo.cs".format(self.dstpath))
		#
		# maincsproj = maincsproj.replace(self.orgname,self.dstprojname)
		# AssemblyInfo = AssemblyInfo.replace(self.orgname,self.dstprojname)
		#
		# neolib.StrToFile(maincsproj,"{0}/{1}.cs".format(self.dstpath,self.dstprojname))
		# neolib.StrToFile(AssemblyInfo,"{0}/Properties/AssemblyInfo.cs".format(self.dstpath))
		#
		# print(maincsproj)


		None
	def changeContentsUnit(self,filename,changeFunction):
		contents = neolib.StrFromFile(filename)

		contents = changeFunction(contents)

		if contents == None : return


		neolib.StrToFile(contents,filename)


	def isFilter2Skip(self,root,basename):
		ext = os.path.splitext(basename)[1]
		if ext not in self.availext: return True
		if "/obj/" in root: return True

		return False
	def doRun(self):
		self.arrayorgpath = self.getLists(self.orgpath)

		self.lista = neolib.MakeDoubleListFromTxt("adts/modulelist4ADTS")
		print(self.lista)

		def changeFunction(contents):
			print(contents)
			#contents = contents.replace(self.orgname, self.dstprojname)
			return None

		#self.changeContentsUnit("{0}/DeviceTesterSystem.sln".format(self.basepath), changeFunction)
		#exit()
		for row in self.lista:
			self.process = row[0]
			self.prefix = row[1]
			self.name = row[2]
			self.uuid = row[3]
			projectname = self.prefix+self.name
			self.dstpath = self.basepath + "/" + projectname
			self.dstprojname = projectname

			self.CopyProject()
			self.ChangeContents()





		# self.CopyProject("Temp2Library")
		# self.CopyProject("Temp3Library")
		# self.CopyProject("Temp4Library")







		None



class AnalyzeInterface(neolib4Win.NeoAnalyzeClasss):
	patterninterface = r'public\s+interface\s+([\w\d_<>]+)\s*(?::\s*([\w\d_<>]+)\s*)*\{([^{}]*)\}'
	patternmethod = r'(\w+)\s*(\s|[\[\]]{2})\s*([\w\d_]+)\(([^\(\)]*)\);'
	patternparam = r'(?:(params|ref)\s+)*([\w]+)(\s|[\[\]]{2})\s*([\w]+)'
	patternProperty = r'(\w+)\s+([\w\d_]+)\s*\{\s*(get|set)\s*;\s*\}'
	patternReserveReverse = r"TAG:(get|set)"
	patterRemoveComment = r'\s*//(.+)\n'


	mapcount = {1:0,2:1,3:3}
	def levelProc(self,str,level):


		if level <= self.prevlevel:
			count = self.mapcount[level]
			self.strlines += "\n"
			self.strlines += "\t" * (count)
			None



		#self.strlines += "(%d)" % (level)
		self.strlines +=str
		self.strlines += "\t"


		self.prevlevel = level

	def doRun(self):

		mapinteface = collections.OrderedDict()
		strorgtxt = neolib.StrFromFile("adts/interface.txt")

		#strorgtxt = strorgtxt.replace("\r","")
		#strorgtxt = strorgtxt.replace("\n", "")

		strorgtxt = re.sub(self.patternProperty,r"TAG:\1",strorgtxt)

		results = re.findall(self.patterninterface,strorgtxt)
		print(results)
		for name,parent,methods in results:
			#print(name)
			#print(methods)
			mapinteface[name] = collections.OrderedDict()
			for ret,pinter,methodname,params in re.findall(self.patternmethod,methods):
				mapinteface[name][methodname] = (collections.OrderedDict(),ret+pinter)

				#print(methodname)
				for prefix, type, pt2, paramname in re.findall(self.patternparam, params):
					mapinteface[name][methodname][0][paramname] =  (prefix, type, pt2)

		self.strlines = ""
		tables = []

		level = 0
		self.prevlevel = 0
		for intefacename,methods in mapinteface.items():
			level += 1

			self.levelProc("{0}".format(intefacename),level)

			for methodname, values in methods.items():
				level += 1
				params = values[0]
				ret  = values[1]

				self.levelProc("{0}\t{1}".format(methodname,ret),level)

				for paramname, others in params.items():
					level += 1
					prefix =  others[0]
					type = others[1]
					pointer = others[2]
					self.levelProc("{3}\t{0} {1} {2}".format(prefix,type,pointer, paramname),level)
					level -= 1

					None

				level -= 1

				#self.levelProc(level)
			level -= 1
					#self.strlines += "{0}\t{1}\t{2}\n".format(intefacename,methodname,paramname)
			#tables.append(newline)
			#self.strlines += "\n"




		print(self.strlines)

		#self.strlines =

class InsertWholeDB(neolib.NeoRunnableClasss):

	def setDefArges(self):
		super(InsertWholeDB, self).setDefArges()
		self.defMapArgs.update({'dbaddress': 'localhost'})


	def doRun(self):
		dbaddress = self.mapArgs['dbaddress']


		DropAndCreateTable(exit=False,dbaddress =dbaddress).Run()


		MakeChannel(exit=False,dbaddress =dbaddress).Run()

		MakeEnvSelection(exit=False,dbaddress =dbaddress).Run()

		MakeEnvSetting(exit=False, dbaddress=dbaddress).Run()


		MakePacketDateType(exit=False,dbaddress =dbaddress).Run()
		MakePacket(exit=False,dbaddress =dbaddress).Run()
		MakePacketDataUnit(exit=False,dbaddress =dbaddress).Run()

		MakeScenarioByProfile(exit=False,dbaddress =dbaddress).Run()
		MakeScenarioLineByProfile(exit=False,dbaddress =dbaddress).Run()

		MakeScenario(deleteTable=False, exit=False,dbaddress =dbaddress).Run()
		MakeScenarioLine(deleteTable=False, exit=False,dbaddress =dbaddress).Run()
		MakeScenarioGroup(deleteTable=False, exit=False,dbaddress =dbaddress).Run()

		MakeDataValueTable(exit=False,dbaddress =dbaddress).Run()

		MakeScenarioEtc(deleteTable=False, exit=False,dbaddress =dbaddress).Run()
		MakeScenarioLineEtc(deleteTable=False, exit=False, dbaddress=dbaddress).Run()


"""
이 클래스는 프로파일 세팅을 시나리오로 만드는 클래스 이다.
"""
#MakeNameFieldsClass().Run()

#MakeCreateTableFor(exit=False).Run()
#MakeDataFieldsClass(exit=True).Run()

#MakeEnvSelection(exit=False).Run()
#MakeEnvSetting(exit=True).Run()

dbaddress= 'localhost'
#dbaddress= '192.168.0.75'


#MakeEnvSelection(exit=False,dbaddress=dbaddress).Run()
#MakeEnvSetting(exit=False, dbaddress=dbaddress).Run()
#MakeScenarioLine(dbaddress=dbaddress).Run()
#MakeScenarioLine().Run()

InsertWholeDB(exit=False).Run()
InsertWholeDB(dbaddress="192.168.0.75").Run()

#AnalyzeInterface().Run()

#MakeCSharpProject().Run()





#MakeScriptSentenceFromMySQL().Run()
#MakeScriptSentenceFromMySQL().Run()
#countProfileFromMySQL().Run()
#checkInitProfilecountProfileFromMySQL().Run()
#adjustProfileConfigFromMySQL().Run()
#ProfileSettings().Run()

# MakeScenario(deleteTable = False,exit = False).Run()
# MakeScenarioLine(deleteTable = False,exit = False).Run()
# exit()

#DropAndCreateTable(exit = False).Run()




#MakeScenarioDBFromOldDB().Run()
#MakeProfileToScenario().Run()


exit()