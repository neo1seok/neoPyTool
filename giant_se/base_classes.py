from neolib import neolib
from neolib import crypto_util
import random
import simplejson as json
import queue
from giant_se.calc_util import *
#factory_key_rtl = "87A294257B61C7A7EC2058725B6D844164309B2465D0F82FB66F316E6B25BAD7"

class BaseRegAuth:
	chip_json_file = 'rsc/chip.json'
	comm_json_file = 'rsc/comm.json'
	server_json_file = 'rsc/server.json'

	comm_figure = neolib.Struct(**{'factory_key_rtl': ''})
	chip_figure = neolib.Struct(**{'puf':'','e_fuse': ''})
	server_figure = neolib.Struct(**{'map_auth_info':{}})


	factory_key_rtl = crypto_util.getrandom(32)
	factory_key_ID = crypto_util.getrandom(32)
	factory_key = crypto_util.sha256(factory_key_ID + factory_key_ID)


	def __init__(self):
		self.init()
	def init(self):
		None

	def write_json(self,file_name,figure):
		print(figure.get_dict())
		neolib.StrToFile(json.dumps(figure.get_dict(), sort_keys=True, indent=4, separators=(',', ': ')),	 file_name)



class BaseProcess(BaseRegAuth):
	trans_data = queue.Queue();
	list_process = []


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
		print("{0}:\n{1}".format(title,value))

class BaseChipSide(BaseSide):
	def init(self):
		self.chip_figure = self.main_class.chip_figure
		self.chip_json_file = self.main_class.chip_json_file
	def calc_authcode(self,radom):
		return calc_code(self.chip_figure.puf, radom, self.chip_figure.e_fuse)

	def prcess_trans_sn(self):
		sn = calc_sn(self.chip_figure.puf, self.chip_figure.e_fuse)
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

if __name__ == '__main__':
	BaseProcess().load_figures()
