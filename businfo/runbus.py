import pymysql
import neolib.neoutil as neolib
import neolib.db as neodb
import time

import  simplejson as json
import re
import collections
import requests
import os
#from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from xml.etree.ElementTree import Element, ElementTree, SubElement, dump, parse, tostring,fromstring


from json import dumps
import xml.etree.ElementTree as  etree

class RunOpeAPI(neolib.NeoRunnableClasss):
	serviceKey = 'n3y8/FJm14PWe7TSJZCW9MPy9oRX0BKgvbJnF8SxaQCK1IFtxKb7pJUSsRSbT1eA84XdWzGbeCNkSc4lqbCHUg=='
	base_url='http://openapi.gbis.go.kr/ws/rest'
	out_str = ''
	station_id ='228000875'
	route_id = '234000026' # 720-2
	route_id = '234000047' #720


	def doRun_old(self):
		from urllib.request import Request, urlopen

		from  urllib.parse import urlencode
		from  urllib.parse import quote_plus

		from urllib.request import urlopen

		url = 'http://openapi.gbis.go.kr/ws/rest/baseinfoservice'

		# queryParams = '?' + urlencode({ quote_plus('ServiceKey') : 'n3y8/FJm14PWe7TSJZCW9MPy9oRX0BKgvbJnF8SxaQCK1IFtxKb7pJUSsRSbT1eA84XdWzGbeCNkSc4lqbCHUg==', quote_plus('routeId') : '', quote_plus('numOfRows') : '999', quote_plus('pageNo') : '1' , quote_plus('startPage') : '1'})
		queryParams = '?' + urlencode({quote_plus(
			'serviceKey'): 'n3y8/FJm14PWe7TSJZCW9MPy9oRX0BKgvbJnF8SxaQCK1IFtxKb7pJUSsRSbT1eA84XdWzGbeCNkSc4lqbCHUg==',
									   quote_plus('numOfRows'): '999', quote_plus('pageNo'): '1',
									   quote_plus('startPage'): '1'})
		print(url + queryParams)
		request = Request(url + queryParams)
		request.get_method = lambda: 'GET'
		response_body = urlopen(request).read()
		print(response_body.decode())

		print('test')
	def doTemplate(self,apiname,title,params):
		params['serviceKey'] = self.serviceKey
		url = self.base_url+'/'+apiname
		print(url)
		r = requests.get(url, params=params)
		print(r.text)
		neolib.StrToFile(r.text,'sample_xml/'+title)

		self.proc_after(title, r.text)
#		root = fromstring(r.text)

#		print(root.tag)



	def doBase(self):
		self.doTemplate('baseinfoservice','baseinfo.xml',{})

	def doArraval(self):
		self.doTemplate('busarrivalservice','arrival.xml', {'stationId':self.station_id,'routeId' : self.route_id})

	def doArravalStations(self):
		self.doTemplate('busarrivalservice/station','arrival_stations.xml', {'stationId': self.station_id})

	def doBusLocations(self):
		self.doTemplate('buslocationservice','bus_location.xml', {'routeId' : self.route_id})

	def init(self):

		rt_json = neolib.StrFromFile('json/route.json')
		list_bus = json.loads(rt_json)
		self.map_route_line = dict([(cols[0],cols )for cols in list_bus])

		st_json = neolib.StrFromFile('json/station.json')
		list_station = json.loads(st_json)
		self.map_station = dict([(cols[0], cols) for cols in list_station])

		None
	def view(self,*args):
		newstrarray = [str(tmp) for tmp in args]
		self.out_str += ' '.join(newstrarray)+"\n"
		#print(*args)
	def view_child(self,parent,depth):
		info = ''
		if parent.tag == 'routeId':
			info = '({0})'.format(self.map_route_line[parent.text][1])
		if parent.tag == 'stationId':
			info = '({0})'.format(self.map_station[parent.text][1])


		self.view('\t'*depth,parent.tag,":",parent.text,info)
		for child in parent:
			self.view_child(child,depth+1)
	def proc_after(self,title,result):
		self.out_str = ''
		self.view('title:', title)
		root = fromstring(result)
		self.view_child(root, 0)
		print(self.out_str)
		dst_path = 'out/' + title.replace('.xml', '.txt')
		neolib.StrToFile(self.out_str, dst_path)

	def doRun(self):
		self.init()
		self.doBase()

		self.doBusLocations()
		self.doArraval()
		self.doArravalStations()
		None

class ParseXml(RunOpeAPI):

	def doTemplate_new(self,apiname,title,params):
		self.view('title:',title)
		fname = 'sample_xml/'+title
		x = parse(fname)
#		ads = etree.tostring(x)
#		print(ads)



	def doTemplate(self,apiname,title,params):
		xml_src = neolib.StrFromFile('sample_xml/'+title)

		self.proc_after(title,xml_src)


		# for child in root:
		# 	print(child.tag)
		# msgBody = root.find('msgBody')
		# for child in msgBody:
		# 	print(child.tag)
		# print(root.find('msgBody').attrib)
class MakeJsonFormFromText(neolib.NeoRunnableClasss):
	# filelist = [
	# 	'area20161202.txt',
	# 	'route20161202.txt',
	# 	'routeline20161202.txt',
	# 	'routestation20161202.txt',
	# 	'station20161202.txt']
	filelist = [
		'area',
		'route',
		'routeline',
		'routestation',
		'station']

	def makeRows(self,rsrc):
		str = neolib.StrFromFile(rsrc, enc='euc-kr')
		cmps = [tmp.split('|') for tmp in str.split('^')]
		return cmps

	def doRun(self):
		for tmp in self.filelist:
			filename = tmp + '20161202.txt'

			rows = self.makeRows('rsc/' + filename)
			#jsonfile = re.sub(r'([a-z]+)\d{4}\d{2}\d{2}\.txt',r'\1.json',tmp)
			jsonfile = tmp + '.json'
			print(jsonfile)
			neolib.StrToFile(json.dumps(rows,ensure_ascii=False), 'json/'+jsonfile);


class MakeColInfoFromJson(MakeJsonFormFromText):


	def doRun(self):
		self.mapCols = collections.OrderedDict()
		for tmp in self.filelist:
			jsonfile = 'json/'+tmp + '.json'
			strcontnts = neolib.StrFromFile(jsonfile)
			listlist = json.loads(strcontnts)

			self.procListList(tmp,listlist)

		self.procFinal()


	def procListList(self,tablename,listlist):
		print("{0}|{1}".format(tablename, ",".join(listlist[0])))
		self.mapCols[tablename]=listlist[0]

	def procFinal(self):

		neolib.StrToFile(json.dumps(self.mapCols, ensure_ascii=False), 'json/colinfo.json' );
		None

class CheckMaxLen(MakeColInfoFromJson):
	maxSize = 0

	def procListList(self,tablename,listlist):

		cols = listlist[0]
		listlistcontents = listlist[1:len(listlist)]
		print(tablename)
		for row in listlistcontents:
			#print(row)
			for col in row:
				#print(len(col))
				self.maxSize = max(len(col),self.maxSize)



	def procFinal(self):

		print(self.maxSize)


		None
class InsertDBFromJson(MakeColInfoFromJson):
	class MakeDB_BASE(neodb.BaseMySQLRunnable):
		def InitRun(self):
			self.dbaddress = self.mapArgs['dbaddress']
			self.listmap = []

			print("dst db:" + self.dbaddress)

			self.dstdbHD = neodb.dbHandleing(host=self.dbaddress, port=3306, user='neo1seok', passwd='tofhdna1pi', db='kbus',
									   charset='utf8')
			None
		def SetColine(self, colline):
			self.colline = colline

		def SetListList(self, listlistcontents):
			self.listlistcontents = listlistcontents

		def processInserValues(self):
			idx = -1;
			maxnum = len(self.listlistcontents)
			for row in self.listlistcontents:
				idx += 1
				maprow = {self.cols[idx]: row[idx] for idx in range(0, len(self.cols))}
				self.listmap.append(maprow)

				if len(self.listmap) > 5000:
					print('%s %d / %d'%(self.dsttable,idx,maxnum))
					self.processInserToDB()
					self.listmap.clear()


		def doRun(self):
			self.strlines = ""
			if self.mapArgs['deleteTable']:
				self.deleteTable()

			self.cols = re.split(r',\s*', self.colline)
			self.listmap = []

			self.processInserValues()

			for row in self.listmap:
				print(row)
			self.processInserToDB()

			self.processAfterDB()

			time.sleep(0.3)

			None



			None


	class MakeDB_area(MakeDB_BASE):
		dsttable = "area";
		prefix = "ara"

	class MakeDB_route(MakeDB_BASE):
		dsttable = "route";
		prefix = "rte"

	class MakeDB_routeline(MakeDB_BASE):
		dsttable = "routeline";
		prefix = "rtl"

	class MakeDB_routestation(MakeDB_BASE):
		dsttable = "routestation";
		prefix = "rts"

	class MakeDB_station(MakeDB_BASE):
		dsttable = "station";
		prefix = "stn"

	def InitRun(self):

		self.mapfilelist =  {
			'area':self.MakeDB_area,
			'route':self.MakeDB_route,
			'routeline':self.MakeDB_routeline,
			'routestation':self.MakeDB_routestation,
			'station':self.MakeDB_station
		}

		print(self.mapfilelist)


	def procListList(self,tablename,listlist):
		print(tablename)
		dbRunhandler = self.mapfilelist[tablename](exit=False,dbaddress="neo1seok.iptime.org")
		cols = listlist[0]
		listlistcontents = listlist[1:len(listlist)]
		dbRunhandler.SetColine(",".join(cols))
		dbRunhandler.SetListList(listlistcontents)
		dbRunhandler.Run()

	def procFinal(self):

		None



class CreateTableAnd(neodb.MakeCreateTableFor):
	xlsDbFile = "TABLE정보.xlsx"
	def doRun(self):
		ret = self.makeMapFromExcel(self.xlsDbFile)
		self.strlines = self.makeSqlDropAndCreate(ret,self.createTableForm,self.fieldForm)
		neolib.StrToFile(self.strlines, "table/TABLE.SQL")
		self.strlines = self.makeSqlDropAndCreate(ret, self.dropTableForm, '')
		neolib.StrToFile(self.strlines, "table/DROP.SQL")

		None



if __name__ != '__main__':
	exit()

# InsertDBFromJson().Run()
# CreateTableAnd().Run()
# CheckMaxLen().Run()
#
# #CreateTableAnd().Run()
#
# MakeColInfoFromJson().Run()
#
#
# MakeJsonFormFromText().Run()

RunOpeAPI().Run()
#ParseXml().Run()


