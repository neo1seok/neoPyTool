from giant_se.base_classes import *
from giant_se.calc_util import *
class Generator(BaseRegAuth):

	def init(self):
		self.map_figureinfo = {
			'comm': (self.comm_figure, self.comm_json_file, self.generate_comm),
			'chip': (self.chip_figure, self.chip_json_file, self.generate_chip),
			'server': (self.server_figure, self.server_json_file, self.generate_server),
		}
		None
	def write_json(self,file_name,figure):
		print(figure.get_dict())
		neoutil.StrToFile(json.dumps(figure.get_dict(), sort_keys=True, indent=4, separators=(',', ': ')), file_name)

	def generate_comm(self,figure):
		#figure.factory_key_rtl  = crypto_util.getrandom(16)
		#figure.factory_key_id = crypto_util.getrandom(2)
		figure.company_no =  'ictk0001'

		#figure.asfdafdsa = '23'
		#self.write_json(self.comm_json_file,self.comm_figure)

	def generate_chip(self,figure):
		figure.puf = "6B534B5A548A1E3EEF8F053B02AD7EF8"#crypto_util.getrandom(16)
		figure.factory_key_rtl = "5C7CCC241E71157F08E1F33D71D1049F"#crypto_util.getrandom(16)
		#figure.e_fuse = crypto_util.getrandom(8)


		figure.sn = calc_sn(figure.puf)
		#self.write_json(self.chip_json_file, self.chip_figure)

	def generate_server(self,figure):
		None

		#self.write_json(self.server_json_file, self.server_figure)
	def mapping_auth_info(self):
		company_no = 'ictk0001'
		self.server_figure.map_company_no_to_factory_key_id = {'ictk0001':{'factory_key_id':'','factory_key':''}}
		self.server_figure.map_factory_key_id_factory_key = {}
		for idx in range(10):
			factorykeyid = crypto_util.getrandom(2)
			FactoryKey = left_16_sha256(factorykeyid + self.chip_figure.factory_key_rtl)
			self.server_figure.map_factory_key_id_factory_key[factorykeyid] = FactoryKey



		self.server_figure.map_company_no_to_factory_key_id[company_no] = factorykeyid


		None
		# sn = calc_sn(self.chip_figure.puf, self.chip_figure.e_fuse)
		# self.server_figure.map_auth_info[sn] =  {
		# 	'factory_key_id':crypto_util.getrandom(2),
		# 	'authcode': '',
		# 	'random': ''
		# }


	def run(self):
		self.factory_key_rtl = crypto_util.getrandom(32)
		for key,values in self.map_figureinfo.items():
			figure,file,gen_proc=values
			gen_proc(figure)

		self.mapping_auth_info()

		for key, values in self.map_figureinfo.items():
			figure, file, gen_proc = values

			self.write_json(file, figure)









if __name__ == '__main__':
	Generator().run()
