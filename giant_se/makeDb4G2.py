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

	def InitRun(self):

		# self.test2(aaa='1',aaa2='2')

		self.dbaddress = self.mapArgs['dbaddress']
		self.listmap = []


		print("dst db:"+self.dbaddress)
		self.dstdbHD = dbHandleing(host='localhost', port=3306, user='ictk', passwd='#ictk1234', db='adts_giant_se',	   charset='utf8')
		self.strlines = ""

		None


	def endRun(self):
		# fb = open('out.txt', 'wb')
		# fb.write(self.strlines.encode())
		# fb.close()
		#
		# neolib4Win.SetClipBoard(self.strlines)

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

		if self.mapArgs['deleteTable']:
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
		self.appendLine(name='OPTION 1', discription='기본 설정')
		None


class MakeEnvSetting(BaseTableInput):
	dsttable = "env_setting"
	colline = "esl_uid,item, value,type,comment"
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
		list_env = [
			('CC_VALUE', '000F20008000340406E10400800000',"VALUE"),
			('AID', 'D2760000850101', "VALUE"),
			('CC_ID', 'E103', "VALUE"),
			('NDEF_ID', 'E104',"VALUE"),
			('GIANT2_AID', 'D4107216700302', "VALUE"),

		]

		for item,value,type in list_env:
			self.appendLine(item=item, value=value, esl_uid=esl_uid, comment="")





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

class MakePacket(BaseTableInput):
	dsttable = "packet";
	prefix = "pck"
	colline = "name, type, discription,  packet_class"

class MakePacketDataUnit(MakePacket):
	dsttable = "packet_data_unit";
	colline = "pck_uid, index, pdt_uid, def_value,comment"
	prefix = "pdu"




#이 클래스는 스마트로의 스크립트 정보를 이용하여
#새로운 커맨드 라인을 만드는 클래스이다.
#adts/cmdmappingTable.txt 에 instruction mapping 정보가
#뉴라인 탭 형태의 테이블 정보로 들어 있다.

class MakeScenario(BaseTableInput):
	dsttable = "scenario"
	prefix = "sce"
	colline = "scg_uid, name, discription, param, param_ext, type, classname,comment"
	srcxlsfile = 'rsc/시나리오.xlsx'

	def processInserValues(self):
		xl_workbook = xlrd.open_workbook(self.srcxlsfile)
		sheet_names = xl_workbook.sheet_names()
		for sheet_name in sheet_names:
			type =''
			if sheet_name == '사전설정':
				type= 'profile'
			self.appendLine(name=sheet_name, scg_uid='scg_1',type=type,classname='GiantSeSC', discription="", comment="")
			# self.appendLine(name="G2 NFC READ 검증",scg_uid='scg_1', discription="", comment="")
			# self.appendLine(name="G2 NFC REG 검증",scg_uid='scg_1' ,discription="", comment="")
			# self.appendLine(name="G2 NFC AUTH 검증",scg_uid='scg_1' ,discription="", comment="")
			# self.appendLine(name="TEST SPI 검증", scg_uid='scg_2', discription="", comment="")
		None

class MakeScenarioLine(BaseTableInput):
	dsttable = "scenario_line"
	prefix = "scl"
	colline = "sce_uid, index, method, title, param, param_ext,pck_uid, comment"
	srcxlsfile = 'rsc/시나리오.xlsx'
	patt_json_set=r'([\w$]+):([\w$]+)'
	def convert_param_ext(self,param_ext):
		#print(param_ext)
		result_list = re.findall(self.patt_json_set,param_ext)
		if len(result_list) ==0:
			return param_ext
		ret = json.dumps(dict(result_list))
		print(ret)
		return ret



	def processInserValues(self):


		xl_workbook = xlrd.open_workbook(self.srcxlsfile)
		sheet_names = xl_workbook.sheet_names()
		print('Sheet Names', sheet_names)
		for sheet_name in sheet_names:
			map_scenarioline = self.dstdbHD.select("""
					SELECT sce_uid FROM scenario where name='{0}';
							""".format(sheet_name))

			sce_uid = map_scenarioline[0]['sce_uid']
			#print(map_scenarioline)
			xl_sheet = xl_workbook.sheet_by_name(sheet_name)
			#print('Sheet name: %s' % xl_sheet.name)
			rows = [tmp for tmp in xl_sheet.get_rows()][1:]
			print("rows:",rows[0])
			lines = [tuple([tmp.value for tmp in row]) for row in rows]

			index = 0
			print(lines)
			for title,method,param,param_ext in lines:

				self.appendLine(sce_uid=sce_uid, index=index, title=title,method=method,param=param,param_ext=self.convert_param_ext(param_ext))
				index += 1



		None


class MakeScenarioGroup(BaseTableInput):
	dsttable = "scenario_group"
	prefix = "scg"
	colline = "scg_uid_parent, name, discription,comment"

	def processInserValues(self):
		self.appendLine(scg_uid_parent="",name="일반 검증", discription="",comment="")
		self.appendLine(scg_uid_parent="", name="TEST API 검증", discription="", comment="")


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


# orgtest = 'comp1:${CC_EF_ID},comp2:$result'
# list_res =  re.findall(r'([\w{}]+):([\w*\{\}\+]+)',orgtest)
# print(list_res)
# exit()

"""
이 클래스는 프로파일 세팅을 시나리오로 만드는 클래스 이다.
"""
#MakeNameFieldsClass().Run()

#MakeCreateTableFor(exit=False).Run()
#MakeDataFieldsClass(exit=True).Run()

# MakeEnvSelection(exit=False).Run()
# MakeEnvSetting(exit=False).Run()
# MakeScenarioGroup(exit=False).Run()
MakeScenario(exit=False).Run()
MakeScenarioLine(exit=False).Run()

dbaddress= 'localhost'
#dbaddress= '192.168.0.75'


#MakeEnvSelection(exit=False,dbaddress=dbaddress).Run()
#MakeEnvSetting(exit=False, dbaddress=dbaddress).Run()
#MakeScenarioLine(dbaddress=dbaddress).Run()


#InsertWholeDB(exit=False).Run()
#InsertWholeDB(dbaddress="192.168.0.75").Run()

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