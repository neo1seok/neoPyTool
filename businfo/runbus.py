import pymysql
import neolib.neolib as neolib
import  simplejson as json
import re

class TestOpeAPI(neolib.NeoRunnableClasss):
	def doRun(self):
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
class MakeJsonFormFromText(neolib.NeoRunnableClasss):
	filelist = [
		'area20161202.txt',
		'route20161202.txt',
		'routeline20161202.txt',
		'routestation20161202.txt',
		'station20161202.txt']

	def doRun(self):
		for tmp in self.filelist:
			rows = makeRows('rsc/' + tmp)
			jsonfile = re.sub(r'([a-z]+)\d{4}\d{2}\d{2}\.txt',r'\1.json',tmp)
			print(jsonfile)
			neolib.StrToFile(json.dumps(rows,ensure_ascii=False), 'json/'+jsonfile);


def makeRows(rsrc):
	str = neolib.StrFromFile(rsrc, enc='euc-kr')
	cmps = [tmp.split('|') for tmp in str.split('^')]
	return cmps



if __name__ != '__main__':
	exit()







#MakeJsonFormFromText().Run()

TestOpeAPI().Run()



