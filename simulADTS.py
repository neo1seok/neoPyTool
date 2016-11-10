import collections
import os
import re

import  simplejson as json

import neolib.neolib as neolib
from makeDb4ADTS import BaseMySQLRunnable


class MakeScriptSentenceFromMySQL(BaseMySQLRunnable):





	def makeMapAllType(self, result_list, data):
		mapvalus = {}
		for id, VFT, value in result_list:
			strid = str(int(id))
			mapvalus[strid] = (VFT, value)
			# 첫번째 loop 결과 ('SooKkaRak', 'gmail', 'com')
			# 두번째 loop 결과 ('Sweeper', 'yahoo', 'com')

			# print(	"{0} {1} {2} {3}".format(strid,newmap[strid]['name'],VFT,value)			  )
			None
		# print(data)
		mapresultvalus = collections.OrderedDict()

		for id in data.split('|'):
			# print(id)
			strvalues = None
			TF = "NOVALUE"
			name = self.mapOldDBMainType[id]['name']
			if id in mapvalus:
				TF = mapvalus[id][0]
				strvalues = mapvalus[id][1]
			mapresultvalus[name] = strvalues
		return mapresultvalus



	def mainProcess(self):

		patt = r'G([0-9]+):(F|T):([0-9A-Za-z가-힣^.,_$=\-+()*\^ ]*)\^\\'


		self.cur.execute(
			"SELECT A.scriptid, instruction, delay, protocol, sentence, etc, direction,testcase,profilename FROM script_maininfo A ,script_sublist B where A.scriptid = B.scriptid and A.devtype = B.devtype and A.devtype = 'V100_EN07' and instruction in ('요청 전문 수신','응답 전문 송신');")
		mapscript = self.cur.fetchall()
		strout = ''
		for tmp in mapscript:
			sentence = tmp['sentence']
			scriptid = tmp['scriptid']
			protocol = tmp['protocol']
			instruction = tmp['instruction']
			direction = tmp['direction']

			result_list = re.findall(patt, sentence)

			remove = re.sub(patt, "", sentence)
			if remove != '':
				print("{0}\t{1}\t{2}\t{3}\t".format(tmp['scriptid'], tmp['testcase'], protocol, remove, sentence))
				continue

			# print(scriptid)
			# print(protocol)

			# mapresultvalus = self.makeMapAllType(result_list,self.newmapprotocol[protocol+direction]['data'])
			mapresultvalus = self.makeMapJustValue(result_list)

			# print("{0}\t{1}\t{3}".format(id,name, TF,strvalues))
			strjson = json.dumps(mapresultvalus, ensure_ascii=False)
			strline = "{0}\t{1}\t{2}\t{3}".format(scriptid, instruction, protocol, strjson)
			self.strlines += strline
			self.strlines += "\r\n"

		# print(strline)
		# print(mapresultvalus)

		# print()
		# neolib.SetClipBoard(strout)





		return

	def initResultMap(self):
		self.mapresult = collections.OrderedDict()
		#self.mapresult = {}
		# collections.OrderedDict()

		for tmp in self.cols:
			self.mapresult[tmp] = ''
		self.mapresult['index'] = self.index
		self.mapresult['protocol'] = self.protocol
		self.mapresult['direction'] = self.direction

		self.index += 1

	def appendLine(self, **kwargs):
		self.initResultMap()
		for key,value in kwargs.items():
			self.mapresult[key] = value

		self.listmap.append(self.mapresult)

		#strline = "{0}\t{1}\t{2}\t\t{3}\t{4}\t{5}\t{6}\t{7}".format(name, length, strv, encoding, chartype, value,	script, order)
		#self.strlines += strline
		#self.strlines += "\n"









class countProfileFromMySQL(BaseMySQLRunnable):

	def mainProcess(self):
		sql = 'SELECT seq, uid, profilename, description, devtype FROM profile_profile_sublist;'
		mapprofile = self.select(sql)

		for tmp in mapprofile:
			self.cur.execute(
				"SELECT count(*) as count,profilename FROM test_smartro.script_sublist where  devtype = 'V100_EN07' and profilename = '{0}';".format(
					tmp['profilename']))

			mapscript = self.cur.fetchone()
			self.append(tmp['profilename'] + "\t" + str(mapscript['count']) + "\t" + tmp['description'])
			None

		None

class checkInitProfilecountProfileFromMySQL(BaseMySQLRunnable):

	def mainProcess(self):

		mapsubscript = self.select("SELECT seq, uid, scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM test_smartro.script_sublist where devtype = 'V100_EN07' ;")


		for tmp in mapsubscript:
			scriptid = tmp['scriptid']
			mapscript = self.select("SELECT seq, uid, scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo where devtype = 'V100_EN07' and scriptid = '{0}';".format(scriptid))
			listinstruction = []
			for tmprow in mapscript:
				listinstruction.append(tmprow['instruction'])

			if 	'설정 초기화' not in listinstruction:
				self.append("{0} {1}".format(scriptid ,listinstruction))

			class checkInitProfilecountProfileFromMySQL(BaseMySQLRunnable):

				def mainProcess(self):

					mapsubscript = self.select(
						"SELECT seq, uid, scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM test_smartro.script_sublist where devtype = 'V100_EN07' ;")

					for tmp in mapsubscript:
						scriptid = tmp['scriptid']
						mapscript = self.select(
							"SELECT seq, uid, scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo where devtype = 'V100_EN07' and scriptid = '{0}';".format(
								scriptid))
						listinstruction = []
						for tmprow in mapscript:
							listinstruction.append(tmprow['instruction'])

						if '설정 초기화' not in listinstruction:
							self.append("{0} {1}".format(scriptid, listinstruction))

						class checkInitProfilecountProfileFromMySQL(BaseMySQLRunnable):

							def mainProcess(self):

								mapsubscript = self.select(
									"SELECT seq, uid, scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM test_smartro.script_sublist where devtype = 'V100_EN07' ;")

								for tmp in mapsubscript:
									scriptid = tmp['scriptid']
									mapscript = self.select(
										"SELECT seq, uid, scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo where devtype = 'V100_EN07' and scriptid = '{0}';".format(
											scriptid))
									listinstruction = []
									for tmprow in mapscript:
										listinstruction.append(tmprow['instruction'])

									if '설정 초기화' not in listinstruction:
										self.append("{0} {1}".format(scriptid, listinstruction))

									class checkInitProfilecountProfileFromMySQL(BaseMySQLRunnable):

										def mainProcess(self):

											mapsubscript = self.select(
												"SELECT seq, uid, scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM test_smartro.script_sublist where devtype = 'V100_EN07' ;")

											for tmp in mapsubscript:
												scriptid = tmp['scriptid']
												mapscript = self.select(
													"SELECT seq, uid, scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo where devtype = 'V100_EN07' and scriptid = '{0}';".format(
														scriptid))
												listinstruction = []
												for tmprow in mapscript:
													listinstruction.append(tmprow['instruction'])

												if '설정 초기화' not in listinstruction:
													self.append("{0} {1}".format(scriptid, listinstruction))

class adjustProfileConfigFromMySQL(BaseMySQLRunnable):
	def mainProcess(self):
		listmapprofileid = self.select(
			"SELECT A.uid,category, profileid,profiletitle,  A.profiletype, value, `option`,A.devtype FROM test_smartro.profile_config_maininfo A,test_smartro.profile_config_sublist B where A.devtype = B.devtype and A.profiletype = B.profiletype and A.devtype = 'V100_EN07'")
		patt = r'^([A-Z]{1,2}[0-9\-]+) (.+)'
		for tmp in listmapprofileid:
			profiletitle = tmp['profiletitle']
			profileid = tmp['profileid']
			uid = tmp['uid']

			#print(tmp['profiletitle'])
			#self.append(tmp['profiletitle'])

			newprofileid = re.sub(patt,r"\2",profiletitle)
			if newprofileid != profileid:
				self.append("{0}|{1}|{2}|{3}".format(uid,newprofileid,profileid,profiletitle))
				self.select(
					"UPDATE profile_config_maininfo SET profileid = '{1}' WHERE uid = '{0}'".format(uid,newprofileid))

class AnalizeScriptFromMySQL(BaseMySQLRunnable):
	def makeOrgListMap(self,strarrayform):

		# listmapcript = self.select(			"SELECT scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo  where devtype = 'V100_EN07' and scriptid in({0})".format(				strarrayform))
		self.listmapcript = self.select(
			"SELECT scriptid, instruction, delay, protocol, sentence, etc, direction, devtype FROM test_smartro.script_maininfo  where devtype = 'V100_EN07' and scriptid like 'STC.%' ")
		# listmapcriptsub = self.select(			"SELECT scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM script_sublist  where devtype = 'V100_EN07' and scriptid in({0})".format(			strarrayform))
		self.listmapcriptsub = self.select(
			"SELECT scriptid, title, script, objective, category, subcategory, caseid, testcase, profilename, devtype FROM script_sublist  where devtype = 'V100_EN07' and scriptid like 'STC.%'".format(
				strarrayform))

	def procMakeMap(self,listwithzero):

		self.mapperscript = {}
		self.maplist = collections.OrderedDict()
		listwithsinglQut = list(map(lambda n: "'"+n+"'",listwithzero))
		strarrayform = ",".join(listwithsinglQut)

		self.makeOrgListMap(strarrayform)

		for tmpmap in self.listmapcriptsub:
			scriptid = tmpmap['scriptid']
			self.mapperscript[scriptid] = tmpmap
			self.maplist[scriptid] = {}
			self.maplist[scriptid]['script'] = tmpmap
			self.maplist[scriptid]['protocol'] = []
			self.maplist[scriptid]['instruction'] = []

		self.mapprotocol = {}
		for tmpmap in self.listmapcript:
			scriptid = tmpmap['scriptid']
			instruction = tmpmap['instruction']
			protocol = tmpmap['protocol']
			sentence = tmpmap['sentence']

			listprotocol = self.maplist[scriptid]['protocol']
			listinstruction = self.maplist[scriptid]['instruction']


			if protocol != '':
				if protocol not in listprotocol:
					mapresultvalus = collections.OrderedDict()
					mapresultvalus['NAME'] = protocol;
					(mapValue,remain) = self.ConvertFromSentence(mapresultvalus,sentence)
					listprotocol.append(mapValue)
					sentence = ""



			listinstruction.append(instruction+"|"+sentence)
			#print(tmpmap["instruction"])

	def removeSame(self,arr,arr2):
		refarr = arr[:]
		refarr2 = arr2[:]

		for tmp in refarr:
			if tmp in refarr2:
#				arr.remove(tmp)
				try:
					arr2.remove(tmp)
				except:
					None

	def removeSameMap(self, arr, arr2):
		refarr = arr[:]
		refarr2 = arr2[:]
		i = -1
		for maplist in refarr:
			i+=1

			for tmpkey,tmpvalue in maplist.items():
				if tmpkey in refarr2 and refarr2[i][tmpkey] == tmpvalue:
					try:
						arr2[i].remove(tmpkey)
					except:
						None

	def mainProcess(self):
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
			listwithzero.append(str)



		self.procMakeMap(listwithzero)






		self.AnalListAll()
		#self.AnslCountCompare()

	def appendDivTabl(self,*args):
		str = ''
		for tmp in args:
			str += "{0}\t".format(tmp)

		self.append(str)



	def AnalListAll(self):
		arr = self.maplist['STC.A.001.00']['instruction'][:]
		mapCaseIdPerTestCase = {}
		reffarr = ['STC.A.001.00', 'STC.A.003.00', 'STC.A.007.00', 'STC.A.008.00', 'STC.A.014.00', 'STC.A.501.00', 'STC.A.601.00', 'STC.A.603.00', 'STC.A.701.00', 'STC.A.702.00',
				   'STC.B.001.00', 'STC.B.501.00', 'STC.B.701.00', 'STC.D.001.00', 'STC.D.701.00', 'STC.P.001.00', 'STC.P.001.02', 'STC.P.001.03', 'STC.P.001.04', 'STC.P.001.05',
				   'STC.A.016.00', 'STC.P.001.06','STC.A.201.30','STC.A.201.61','STC.A.606.00']

		for scriptid, v in self.maplist.items():
			listprotocol = v['protocol']
			listinstruction = v['instruction']
			mapscript = v['script']

			testcase = mapscript['testcase']
			caseid = mapscript['caseid']
			profilename = mapscript['profilename']
			if scriptid in reffarr:
				mapCaseIdPerTestCase[scriptid] = listinstruction[:], listprotocol[:];
		#		print(caseid,scriptid)




		for scriptid,v in self.maplist.items():
			listprotocol = v['protocol']
			listinstruction = v['instruction']
			mapscript = v['script']

			testcase = mapscript['testcase']
			caseid = mapscript['caseid']
			profilename  = mapscript['profilename']

			if scriptid in mapCaseIdPerTestCase:
				reflist = mapCaseIdPerTestCase[scriptid][0]
				refprotomap = mapCaseIdPerTestCase[scriptid][1]

				refscriptid = scriptid
				isreff = True
			else:
				self.removeSame(reflist, listinstruction)
				self.removeSameMap(refprotomap,listprotocol)
				isreff = False


			#refscriptid = mapCaseIdPerTestCase[caseid][0]
			#reflist = mapCaseIdPerTestCase[caseid][1]


#			protarray = self.mapprotocol[k]
			self.appendDivTabl(caseid,scriptid,testcase,isreff,listinstruction,json.dumps(listprotocol, ensure_ascii=False),len(listinstruction),profilename)
			#self.append("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(caseid,k,obj,protarray,v,len(v),profilename))
			#print("{0}\t{1}\t{2}".format(k,obj,v))
	def AnslCountCompare(self):
		self.newmapCount = collections.OrderedDict()

		for k, v in self.maplist.items():
			obj = v["script"]['testcase']
			caseid = v["script"]['caseid']
			profilename = v["script"]['profilename']

			if caseid not in self.newmapCount:
				self.newmapCount[caseid] = {}
				self.newmapCount[caseid]['count'] = []
				self.newmapCount[caseid]['profilename'] = []

			if profilename not in self.newmapCount[caseid]['profilename']:
				self.newmapCount[caseid]['profilename'].append(profilename)

			if len(v) not in self.newmapCount[caseid]['count']:
				self.newmapCount[caseid]['count'].append(len(v))

		for k,v in self.newmapCount.items():
			self.append("{0}\t{1}\t{2}".format(k, v['count'],v['profilename']))




		None

class ProfileSettings2(BaseMySQLRunnable):
	def repl(self,m):

		return m.group(1).replace("\n","")
	def mainProcess(self):
		patt =r'"([A-Za-z가-힣0-9=.()\n\[\]? ]*)"'
		fb = open('inputmenu.txt', 'rb')
		str = fb.read().decode().replace("\r\n","\n")
		fb.close()

		resultstr = re.sub(patt,self.repl, str)
		self.append(resultstr)




class ProfileSettings(BaseMySQLRunnable):
	def mainProcess(self):
		fb = open('input.txt','rb')
		data = fb.read()
		fb.close()
		#patt = r"([\!가 - 힣A - Za - z0 - 9 + & /]+)[, |\n()]"
		patt = r'\s*([\!가-힣A-Za-z0-9+&/ ]+)[,|\n()]'

		newstr = ''




		for tmp in data.decode().split('\r\n'):
			comps = tmp.split('\t')
			if len(comps) != 3 :continue

			newstr += comps[2]
			newstr += ","

			#self.append(comps[2])

		result_list = re.findall(patt, newstr)
		remain = re.sub(patt,'', newstr)

		print(remain)
		for id in result_list:
			self.append(id)



		None

class ProfileSettings2(BaseMySQLRunnable):
	def mainProcess(self):
		fb = open('input.txt', 'rb')
		data = fb.read()
		fb.close()
		# patt = r"([\!가 - 힣A - Za - z0 - 9 + & /]+)[, |\n()]"
		patt = r'\s*([\!가-힣A-Za-z0-9+&/ ]+)[,|\n()]'

		newstr = ''

		for tmp in data.decode().split('\r\n'):
			comps = tmp.split('\t')
			if len(comps) != 3: continue

			newstr += comps[2]
			newstr += ","

		# self.append(comps[2])

		result_list = re.findall(patt, newstr)
		remain = re.sub(patt, '', newstr)

		print(remain)
		for id in result_list:
			self.append(id)

		None

class ListFileExt(neolib.NeoRunnableClasss):
	def doRun(self):
		list = []
		for root, dirs, files in os.walk("D:\\PROJECT\\자동단말기검수\\REF\\scripts"):
			for basename in files:
				ext = basename.split(".")[-1]
				if ext in list: continue
				list.append(ext)
				print(ext)


		print(list)
		#fb = open('out.txt', 'wb')
		#fb.write(self.strlines.encode())
		#fb.close()



class MakePacketInfoFromMySQL(MakeScriptSentenceFromMySQL):

	def mainProcess(self):
		self.curdst.execute('DELETE FROM adts.packet;')
		self.curdst.execute('DELETE FROM adts.data_unit;')

		self.strlines = ''
		self.cols = ['index',  'name', 'length', 'variation', 'key_index', 'value_encoding',
					 'char_range', 'fixed_value', 'param', 'param_ext', 'regexp']

		row = self.mapOldDBMainProtocol["MS승인D2A"]

		lastseq = self.lastSeq(self.curdst, 'PACKET')
		lastseq += 1

		lastseqDataUnit = self.lastSeq(self.curdst, 'DATA_UNIT')
		lastseqDataUnit += 1

		sqldstfmt = "INSERT INTO adts.packet (seq, pck_uid, name,type, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment) VALUES (%d, '%s','%s', '%s', '%s', '%s', '%s', '%s', now(), now(), '');"
		sqldstfmtDataUnit = "INSERT INTO adts.data_unit (seq, dtu_uid, pck_uid, `index`, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment) VALUES (%d, '%s', '%s', %d, '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', now(), now(), '');"

		self.maplist = collections.OrderedDict()
		for key, value in self.mapOldDBMainProtocol.items():
			self.listmap = []
			self.checkPacketForm(value)
			self.maplist[key] = self.listmap

		for key, value in self.maplist.items():

			protocol = value[0]['protocol']
			direction = value[0]['direction']
			tail = '수신' if direction == 'D2A'  else '송신'
			name = protocol + " " + tail;
			pck_uid = 'pck_'+str(lastseq)

			print(sqldstfmt)

			sql = sqldstfmt% (lastseq, pck_uid, name,'MAIN','','smatro_sc.py','MAKE_PACKET_MAIN','CONFRIM_PACKET_MAIN')

			#seq, pck_uid, name, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment
			lastseq += 1
			self.curdst.execute(sql)




			self.append('====================================')
			self.append(name)
			self.append('====================================')




			index = 0
			for mapresult in value:
				# self.append('====================================')
				strtmp = ''
				for tmpcol in self.cols:
					strtmp += "{0}\t".format(mapresult[tmpcol])
				# self.append("{0}\t".format(mapresult[tmpcol]))
				self.append(strtmp)
				dtu_uid = 'dtu_'+str(lastseqDataUnit)

				sql = sqldstfmtDataUnit%(lastseqDataUnit,dtu_uid,pck_uid,index,mapresult['name'],int(mapresult['length']),mapresult['variation'],mapresult['value_encoding'],mapresult['char_range'],mapresult['fixed_value'],mapresult['param'],mapresult['param_ext'])
				#print(sqldstfmtDataUnit)
				index += 1
				lastseqDataUnit += 1
				self.curdst.execute(sql)
			#seq, dtu_uid, pck_uid, `index`, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment


		# self.makeNewTypeScripFromNotAcqured()

		None

	def getValue(self, key, maps):
		if key not in maps: return ''
		return maps[key]

	def checkPacketForm(self, row):

		self.index = 0;
		datas = row['data']
		self.servicecode = row['servicecode']
		self.protocol = row['protocol']
		self.direction = row['direction']

		# self.append('KEY: {0} {1}'.format(self.protocol,self.direction))


		self.appendLine(name="STX", length="1", encoding='HEX', value="02")
		for tmpindex in datas.split('|'):
			self.processDataTypes(self.mapOldDBMainType[tmpindex])
		self.appendLine(name="ETX", length="1", encoding='HEX', value="03")
		self.appendLine(name="CRC", length="2", encoding='HEX', script='CALC_CRC')

		# neolib.SetClipBoard(self.strlines)





		# print(row['protocol'] + "\n" + self.strlines)

		None

	def processDataTypes(self, datamap):
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
			value = self.servicecode[0:4]
			None
		elif name == '거래구분코드':
			value = self.servicecode[4:6]
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

		self.appendLine(name=name, length=length, variation=strv, value_encoding='ASCII', chartype=chartype, fixed_value=value,
						param=strparam, param_ext=order)

#이 클래스는 스마트로의 스크립트 정보를 이용하여
#새로운 커맨드 라인을 만드는 클래스이다.
#rsc/cmdmappingTable.txt 에 instruction mapping 정보가
#뉴라인 탭 형태의 테이블 정보로 들어 있다.

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
		lastseq = self.lastSeq(self.curdst, 'scenario')
		lastseq += 1

		mapret = self.makeMapCmdFromInputSrc()
		self.listmapcript = self.select(
			"SELECT A.scriptid, instruction, delay, protocol, sentence, etc, direction,B.caseid,B.objective,A.devtype,B.profilename,C.description FROM test_smartro.script_maininfo A,test_smartro.script_sublist B,test_smartro.profile_profile_sublist C where A.devtype = B.devtype and A.devtype = C.devtype and A.scriptid = B.scriptid and A.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용')")
		self.listmapcriptsub = self.select(
			"SELECT B.scriptid, title, script, objective, category, subcategory, caseid, testcase, B.profilename,  C.description "
			"FROM test_smartro.script_sublist B,test_smartro.profile_profile_sublist C where B.devtype = C.devtype and B.devtype = 'V100_EN07' and B.profilename = C.profilename and category in ('00.UTILITY','01.신용');")

		listmapmethodline = self.selectExt(self.curdst,
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
		self.selectExt(self.curdst, "DELETE FROM scenario ;DELETE FROM method_line")


	def InsertScenarioAndMethodLine(self,mapScriptPerScenarioAndMethodLine):

		lastseq = self.lastSeq(self.curdst, 'scenario')
		lastseq += 1

		lastseqMethodLine = self.lastSeq(self.curdst, 'method_line')
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
			self.selectExt(self.curdst, sql)

			index = 0
			for method, title, param, param_ext,pck_uid in values['method_line']:
				self.appendA(method, title, param, param_ext)
				curuidMethodLine = 'mtd_' + str(lastseqMethodLine)
				param = param.replace("'", "\\'")
				param_ext = param_ext.replace("'", "\\'")
				sql = sqldstfmtMethodLine % (
					lastseqMethodLine, curuidMethodLine, curuid, index, method, title, param, param_ext,pck_uid, '')

				print(sql)
				self.selectExt(self.curdst, sql)
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







		return

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
		lastseq = self.lastSeq(self.curdst, 'scenario')
		lastseq += 1


		listmap = self.select(
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

class MakePacketInfoFromMySQLOld(MakePacketDateType):

	def mainProcess(self):
		self.curdst.execute('DELETE FROM adts.packet;')
		self.curdst.execute('DELETE FROM adts.data_unit;')

		self.strlines = ''

		row = self.mapOldDBMainProtocol["MS승인D2A"]

		lastseq = self.dstdbHD.lastSeq('PACKET')
		lastseq += 1

		lastseqDataUnit = self.dstdbHD.lastSeq('DATA_UNIT')
		lastseqDataUnit += 1

		sqldstfmt = "INSERT INTO adts.packet (seq, pck_uid, name,type, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment) VALUES (%d, '%s','%s', '%s', '%s', '%s', '%s', '%s', now(), now(), '');"
		sqldstfmtDataUnit = "INSERT INTO adts.data_unit (seq, dtu_uid, pck_uid, `index`, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment) VALUES (%d, '%s', '%s', %d, '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', now(), now(), '');"

		self.maplist = collections.OrderedDict()
		for key, value in self.mapOldDBMainProtocol.items():
			self.listmap = []
			self.checkPacketForm(value)
			self.maplist[key] = self.listmap

		for key, value in self.maplist.items():

			protocol = value[0]['protocol']
			direction = value[0]['direction']
			tail = '수신' if direction == 'D2A'  else '송신'
			name = protocol + " " + tail;
			pck_uid = 'pck_' + str(lastseq)

			print(sqldstfmt)

			sql = sqldstfmt % (
			lastseq, pck_uid, name, 'MAIN', '', 'smatro_sc.py', 'MAKE_PACKET_MAIN', 'CONFRIM_PACKET_MAIN')

			# seq, pck_uid, name, discription, script_file, make_class, confirm_class, updt_date, reg_date, comment
			lastseq += 1
			self.dstdbHD.execute(sql)

			self.append('====================================')
			self.append(name)
			self.append('====================================')

			index = 0
			for mapresult in value:
				# self.append('====================================')
				strtmp = ''
				for tmpcol in self.cols:
					strtmp += "{0}\t".format(mapresult[tmpcol])
				# self.append("{0}\t".format(mapresult[tmpcol]))
				self.append(strtmp)
				dtu_uid = 'dtu_' + str(lastseqDataUnit)

				sql = sqldstfmtDataUnit % (
				lastseqDataUnit, dtu_uid, pck_uid, index, mapresult['name'], int(mapresult['length']),
				mapresult['variation'], mapresult['value_encoding'], mapresult['char_range'],
				mapresult['fixed_value'], mapresult['param'], mapresult['param_ext'])
				# print(sqldstfmtDataUnit)
				index += 1
				lastseqDataUnit += 1
				self.dstdbHD.execute(sql)
			# seq, dtu_uid, pck_uid, `index`, name, length, variation, value_encoding, char_range, fixed_value, param, param_ext, updt_date, reg_date, comment

		# self.makeNewTypeScripFromNotAcqured()

		None

	def appendLine(self, **kwargs):

		mapresult = collections.OrderedDict()
		# self.mapresult = {}
		# collections.OrderedDict()

		for tmp in self.cols:
			mapresult[tmp] = ''
		mapresult['index'] = self.index
		mapresult['protocol'] = self.protocol
		mapresult['direction'] = self.direction

		self.index += 1

		for key, value in kwargs.items():
			mapresult[key] = value

		self.listmap.append(mapresult)

	def checkPacketForm(self, row):

		self.index = 0;
		datas = row['data']
		self.servicecode = row['servicecode']
		self.protocol = row['protocol']
		self.direction = row['direction']

		# self.append('KEY: {0} {1}'.format(self.protocol,self.direction))


		self.appendLine(name="STX", length="1", encoding='HEX', value="02")
		for tmpindex in datas.split('|'):
			self.processDataTypes(self.servicecode, self.mapOldDBMainType[tmpindex])
		self.appendLine(name="ETX", length="1", encoding='HEX', value="03")
		self.appendLine(name="CRC", length="2", encoding='HEX', script='CALC_CRC')

		# neolib.SetClipBoard(self.strlines)





		# print(row['protocol'] + "\n" + self.strlines)

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
			listmenu = list(filter(lambda x: len(x) > 4, mapobj))
			for cond, inst, newinst, title, param, param_ext, input_value in listmenu:
				mapret[inst] = cond, newinst, title, param, param_ext, input_value
			return mapret

		def ConvertValue(self, value, mapRows, input_value):
			arrayparam = json.loads(input_value)
			newarrayparam = []
			for tmp in arrayparam:
				newarrayparam.append(mapRows[tmp])

			return value.format(*newarrayparam)

		def makeMapScriptPerScenarioAndMethodLineFromOldDB(self):
			lastseq = self.dstdbHD.lastSeq('scenario')
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
						'SMARTRO_SC', profilename,
						objective)  # ( 'name', 'discription', 'profile_sc', 'profile_reset_sc', 'script_file', 'classname')
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
						packetname = protocol + " 수신"
						pck_uid = mapmapmethodline[packetname]['pck_uid']
						arrayMethodLine.append(('RECV', '수신', '$PORT00', '', ''));
						arrayMethodLine.append(('CONFIRM_PACKET', title, param, '', pck_uid));
						# self.appendA('RECV', '수신', '$PORT00')
						# self.appendA('CONFIRM_PACKET', title, param, '{"TYPE":"MAIN","PAKCET":"%s"}' % tmprow['protocol'])

						None
					elif "송신" in instruction:
						packetname = protocol + " 송신"
						pck_uid = mapmapmethodline[packetname]['pck_uid']

						arrayMethodLine.append(('MAKE_PACKET', title, param, '', pck_uid));
						arrayMethodLine.append(('SEND', '송신', '$PORT00', '', ''));
						# self.appendA('MAKE_PACKET', title, param, '{"TYPE":"MAIN","PAKCET":"%s"}' % tmprow['protocol'])
						# self.appendA('SEND', '송신', '$PORT00')
						None

					continue
				arrayMethodLine.append((newinst, title, param, '', ''));
			# self.appendA(newinst, title, param)
			# self.appendA("================================================")


			return mapScriptPerScenarioAndMethodLine

		def makeJsonFile(self):
			mapScriptPerScenarioAndMethodLine = self.makeMapScriptPerScenarioAndMethodLineFromOldDB()
			strjson = json.dumps(mapScriptPerScenarioAndMethodLine, ensure_ascii=False)

			neolib.StrToFile(strjson, 'rsc/mapScriptPerScenarioAndMethodLine.json')

		def deleteScenarioAndMethodLine(self):
			self.dstdbHD.select("DELETE FROM scenario ;DELETE FROM method_line")

		def InsertScenarioAndMethodLine(self, mapScriptPerScenarioAndMethodLine):

			lastseq = self.dstdbHD.lastSeq('scenario')
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
				self.dstdbHD.excute(sql)

				index = 0
				for method, title, param, param_ext, pck_uid in values['method_line']:
					self.appendA(method, title, param, param_ext)
					curuidMethodLine = 'mtd_' + str(lastseqMethodLine)
					param = param.replace("'", "\\'")
					param_ext = param_ext.replace("'", "\\'")
					sql = sqldstfmtMethodLine % (
						lastseqMethodLine, curuidMethodLine, curuid, index, method, title, param, param_ext, pck_uid,
						'')

					print(sql)
					self.dstdbHD.excute(sql)
					# seq  ,mtd_uid  ,sce_uid  ,`index`  ,method  ,title  ,param  ,param_ext  ,updt_date  ,reg_date  ,comment
					index += 1
					lastseqMethodLine += 1

				self.appendA("================================================")

		def mainProcess(self):

			self.deleteScenarioAndMethodLine()
			# return


			self.makeJsonFile()
			strjson = neolib.StrFromFile('rsc/mapScriptPerScenarioAndMethodLine.json')
			mapScriptPerScenarioAndMethodLine = json.loads(strjson);

			self.InsertScenarioAndMethodLine(mapScriptPerScenarioAndMethodLine)
#MakeScriptSentenceFromMySQL().Run()
#MakeScriptSentenceFromMySQL().Run()
#countProfileFromMySQL().Run()
#checkInitProfilecountProfileFromMySQL().Run()
#adjustProfileConfigFromMySQL().Run()
#ProfileSettings().Run()


#MakePacketInfoFromMySQL().Run()
#MakeScenarioDBFromOldDB().Run()
MakeProfileToScenario().Run()






exit()