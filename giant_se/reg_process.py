from giant_se.base_classes import *

class RegProcessChipSide(BaseChipSide):
	def prcess_trans_nonce_cipher(self):
		factorykeyid = self.trans_data.get()
		Random = crypto_util.getrandom(16)
		Nonce = crypto_util.getrandom(16)
		Authcode =  self.calc_authcode(Random)
		self.print_view(locals(), 'factorykeyid')
		self.print_view(locals(), 'Random')
		self.print_view(locals(), 'Nonce')
		self.print_view(locals(), 'Authcode')
		# Authcode = crypto_util.sha256(
		# 	self.chip_figure.puf+Random+self.chip_figure.e_fuse
		# )
		# calc_puf(self.chip_figure.puf,Random,self.chip_figure.e_fuse)


		FactoryKey = left_16_sha256(factorykeyid + self.comm_figure.factory_key_rtl)
		hash_param = crypto_util.sha256(Nonce + FactoryKey)
		Random_Authcode = Random+Authcode
		self.print_view(locals(), 'FactoryKey')
		self.print_view(locals(), 'hash_param')
		self.print_view(locals(), 'Random_Authcode')
		Cither = crypto_util.xor_calc(Random_Authcode, hash_param)
		self.print_view(locals(), 'Cither')

		self.trans_data.put(Nonce)
		self.trans_data.put(Cither)



class RegProcessServerSide(BaseServerSide):
	def prcess_factory_key_id(self):
		sn = self.trans_data.get()
		company_no = self.trans_data.get()
		#factory_key_id = self.trans_data.get()

		self.auth_info = neolib.Struct(**{})

		#self.extract_map_auth_info_from_sn(sn)
		self.auth_info.sn = sn

		#self.auth_info.factory_key_id = ''

		# map_auth_info = self.server_figure.map_auth_info[sn]
		# self.auth_info = neolib.Struct(**map_auth_info)
		#
		# self.auth_info.sn = sn
		# # self.factorykeyid = self.auth_info.factory_key_id
		# # print(sn,self.factorykeyid)

		self.trans_data.put(self.auth_info.factory_key_id)

	def prcess_register(self):
		Nonce = self.trans_data.get()
		Cither = self.trans_data.get()
		self.print_view(locals(), 'Nonce')
		self.print_view(locals(), 'Cither')

		FactoryKey = crypto_util.sha256(self.auth_info.factory_key_id  + self.comm_figure.factory_key_rtl)
		hash_param = crypto_util.sha256(Nonce + FactoryKey)
		self.print_view(locals(), 'FactoryKey')
		self.print_view(locals(), 'hash_param')

		Random_Authcode = crypto_util.xor_calc(Cither, hash_param)
		self.print_view(locals(), 'Random_Authcode')

		self.auth_info.random = crypto_util.substr(Random_Authcode,0,16)
		self.auth_info.authcode =  crypto_util.substr(Random_Authcode,16,48)
		self.update_authinfo()
		# self.server_figure.map_auth_info[self.auth_info.sn] = self.auth_info.get_dict()
		# self.main_class.write_json(self.main_class.server_json_file,self.server_figure)
		#
		# print("Random_Authcode",Random_Authcode)

		None

class RegProcessServerSideWithWebServer(BaseServerSideWithWebServer):
	sublet = 'reg'
	def prcess_factory_key_id(self):
		sn = self.trans_data.get()
		company_no = self.trans_data.get()

		result = self.req_post({"cmd":"FACTORY_KEY_ID","params":{"sn":sn,"company_no":company_no}})


	def prcess_register(self):
		nonce = self.trans_data.get()
		cipher = self.trans_data.get()
		result = self.req_post({"cmd": "REGISTER", "params": {"nonce": nonce, "cipher": cipher}})

class RegProcess(BaseProcess):

	def init(self):
		BaseProcess.init(self)
		self.set_sideclass()
		# self.server_side = RegProcessServerSide(self)
		# self.chip_side = RegProcessChipSide(self)

		self.list_process =  [
			self.chip_side.prcess_get_sn,
			self.trans_company_no,

			self.server_side.prcess_factory_key_id,
			self.trans_factory_key,
			self.chip_side.prcess_trans_nonce_cipher,
			self.server_side.prcess_register
		]

		None
	def set_sideclass(self):
		self.server_side = RegProcessServerSide(self)
		self.chip_side = RegProcessChipSide(self)

	def trans_company_no(self):
		self.trans_data.put(self.comm_figure.company_no)
		#self.trans_data.set(self.comm_figure.factory_key_id)

	def trans_factory_key(self):
		self.trans_data.put(self.comm_figure.factory_key_id)
		#self.trans_data.set(self.comm_figure.factory_key_id)


class RegProcessWithWebServer(RegProcess):

	def set_sideclass(self):
		self.server_side = RegProcessServerSideWithWebServer(self)
		self.chip_side = RegProcessChipSide(self)


if __name__ == '__main__':
	#RegProcess().run()
	RegProcessWithWebServer().set_puf(crypto_util.getrandom(16)).run()