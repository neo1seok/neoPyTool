from neolib import neolib
from neolib import crypto_util
import random
import simplejson as json
import queue
import requests
from giant_se.calc_util import *
#factory_key_rtl = "87A294257B61C7A7EC2058725B6D844164309B2465D0F82FB66F316E6B25BAD7"
from logging import handlers

class BaseRegAuth:
	chip_json_file = 'rsc/chip.json'
	comm_json_file = 'rsc/comm.json'
	server_json_file = 'rsc/server.json'




	def __init__(self,logger=None):
		self.comm_figure = neolib.Struct(**{'factory_key_rtl': ''})
		self.chip_figure = neolib.Struct(**{'puf': '', 'e_fuse': ''})
		self.server_figure = neolib.Struct(**{'map_auth_info': {}})

		self.factory_key_rtl = crypto_util.getrandom(32)
		self.factory_key_ID = crypto_util.getrandom(32)
		self.factory_key = crypto_util.sha256(self.factory_key_ID + self.factory_key_ID)

		self.logger = logger
		if self.logger == None:
			self.logger = FakeLog()
		self.init()



	def init(self):
		None

	def write_json(self,file_name,figure):
		print(figure.get_dict())
		neolib.StrToFile(json.dumps(figure.get_dict(), sort_keys=True, indent=4, separators=(',', ': ')),	 file_name)

class FakeLog:
	def debug(self,fmt,*args):
		#msg = fmt % (*args,)
		print(fmt)
		None



class BaseProcess(BaseRegAuth):
	def load_figures(self):
		for key, values in self.map_figureinfo.items():
			figure, file = values
			figure.from_dict(json.loads(neolib.StrFromFile(file)))
			print(figure.get_dict())


	def init(self):
		self.map_figureinfo = {
			'comm': (self.comm_figure, self.comm_json_file),
			'chip': (self.chip_figure, self.chip_json_file),
			'server': (self.server_figure, self.server_json_file),
		}
		self.load_figures()
		self.trans_data = queue.Queue();

		#self.handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')

		#neolib.create_logger(self.__class__.__name__, handler=self.handler)



		self.list_process = []
	def set_loggger(self, logger):
		self.logger = logger
		print("puf:",logger)
		return self
	def set_puf(self, puf):
		self.chip_figure.puf = puf
		print("puf:",puf)
		return self
	def run(self):
		for proc in self.list_process:
			print(proc.__name__)
			proc()


class BaseSide():
	def __init__(self,main_class):

		self.main_class =main_class
		self.trans_data = main_class.trans_data
		self.server_json_file = self.main_class.server_json_file
		self.comm_figure = self.main_class.comm_figure

		self.logger = main_class.logger

		self.logger.debug("%s __init__", self.__class__.__name__)
		self.init()
	def init(self):
		None

	def prcess_sample(self):
	#	self.trans_data[]
		print('prcess_sample')
		param = self.trans_data.get()

		self.trans_data.put(self.param)
	def print_view(self,localmap,title):
		value = localmap[title]
		#print("{0}:\n{1}".format(title,value))
		self.logger.debug("{0}:\n{1}".format(title,value))

class BaseChipSide(BaseSide):
	def init(self):
		self.chip_figure = self.main_class.chip_figure
		self.chip_json_file = self.main_class.chip_json_file
	def calc_authcode(self,radom):
		print("calc_authcode  puf:",self.chip_figure.puf)
		return calc_code(self.chip_figure.puf, radom)

	def prcess_get_sn(self):
		sn = calc_sn(self.chip_figure.puf)
		self.print_view(locals(),'sn')
		self.trans_data.put(sn)
		None

class BaseServerSide(BaseSide):
	def init(self):
		self.server_figure = self.main_class.server_figure
		self.server_json_file = self.main_class.server_json_file

	def extract_map_auth_info_from_sn(self,sn):
		map_auth_info = self.server_figure.map_auth_info[sn]
		self.auth_info = neolib.Struct(**map_auth_info)
		self.auth_info.sn = sn

	def update_authinfo(self):
		self.server_figure.map_auth_info[self.auth_info.sn] = self.auth_info.get_dict()
		self.main_class.write_json(self.main_class.server_json_file,self.server_figure)
class BaseServerSideWithWebServer(BaseServerSide):
	address = 'neo1seok.pe.kr'
	sublet = ''
	def init(self):
		BaseServerSide.init(self)
		self.session_id = crypto_util.getrandom(16)
		self.ssess = requests.session()



	def req_post(self,jsonvalue):
		jsonvalue['session_id'] = self.session_id
		self.logger.debug(jsonvalue)
		r = self.ssess.post('http://{0}:8080/giant_se/{1}.do'.format(self.address,self.sublet),				data={'json': json.dumps(jsonvalue)})
		self.logger.debug("req_post:%s",r.text)



		return json.loads(r.text)


if __name__ == '__main__':
	BaseProcess().load_figures()
