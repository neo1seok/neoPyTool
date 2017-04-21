from giant_se.base_classes import *
from giant_se.chip_side import *




class RegProcessServerSide(BaseServerSide):
	def prcess_factory_key_id(self):
		sn = self.trans_data.get()
		company_no = self.trans_data.get()

		factorykeyid = self.server_figure.map_company_no_to_factory_key_id[company_no]
		factorykey = self.server_figure.map_factory_key_id_factory_key[factorykeyid]

		#factory_key_id = self.trans_data.get()

		self.auth_info = neolib.Struct(**{})

		#self.extract_map_auth_info_from_sn(sn)
		self.auth_info.sn = sn
		self.auth_info.factory_key = factorykey



		#self.auth_info.factory_key_id = ''

		# map_auth_info = self.server_figure.map_auth_info[sn]
		# self.auth_info = neolib.Struct(**map_auth_info)
		#
		# self.auth_info.sn = sn
		# # self.factorykeyid = self.auth_info.factory_key_id
		# # print(sn,self.factorykeyid)

		self.trans_data.put(factorykeyid)

	def prcess_register(self):
		Nonce = self.trans_data.get()
		Cither = self.trans_data.get()
		mac = self.trans_data.get()
		self.print_view(locals(), 'Nonce')
		self.print_view(locals(), 'Cither')

		FactoryKey = self.auth_info.factory_key
		hash_param = crypto_util.sha256(Nonce + FactoryKey)
		self.print_view(locals(), 'FactoryKey')
		self.print_view(locals(), 'hash_param')

		Random_Authcode = crypto_util.xor_calc(Cither, hash_param)
		self.print_view(locals(), 'Random_Authcode')

		self.auth_info.random = crypto_util.substr(Random_Authcode,0,16)
		self.auth_info.authcode = crypto_util.substr(Random_Authcode,16,48)
		random_server = crypto_util.substr(Random_Authcode,0,16)
		self.trans_data.put(self.auth_info.random)
		self.trans_data.put(random_server)
		self.RandomS = random_server
		calc_mac = left_8_sha256(Random_Authcode)

		if mac != calc_mac:
			raise Exception('result is differnet')
		#self.update_authinfo()
		# self.server_figure.map_auth_info[self.auth_info.sn] = self.auth_info.get_dict()
		# self.main_class.write_json(self.main_class.server_json_file,self.server_figure)
		#
		# print("Random_Authcode",Random_Authcode)
	def final_update(self):
		cipher = self.trans_data.get()
		mac = self.trans_data.get()


		#newRandom, newAuthcode, calc_mac = self.calc_auth(self.auth_info.random, self.auth_info.authcode, self.RandomS,  cipher)
		hash_param, tRandom, newRandom, newAuthcode, calc_mac = self.calc_auth(self.auth_info.random,self.auth_info.authcode, self.RandomS,cipher)

		self.print_view(locals(), 'hash_param')
		# self.print_view(locals(), 'tRandom_newAuthcode')
		self.print_view(locals(), 'tRandom')
		self.print_view(locals(), 'newRandom')
		self.print_view(locals(), 'newAuthcode')
		self.print_view(locals(), 'calc_mac')



		if mac != calc_mac:
			raise Exception('result is differnet')


		self.update_authinfo()
		None

class RegProcessServerSideWithWebServer(BaseServerSideWithWebServer):
	sublet = 'reg'
	def prcess_factory_key_id(self):
		sn = self.trans_data.get()
		company_no = self.trans_data.get()

		result = self.req_post({"cmd":"FACTORY_KEY_ID","params":{"sn":sn,"company_no":company_no}})
		params = result['params']
		self.trans_data.put(params['factory_key_id'])


	def prcess_register(self):
		nonce = self.trans_data.get()
		cipher = self.trans_data.get()
		mac = self.trans_data.get()
		result = self.req_post({"cmd": "REGISTER", "params": {"nonce": nonce, "cipher": cipher,"mac":mac}})

		params = result['params']

		# self.trans_data.put(params['random'])
		# self.trans_data.put(params['random_server'])


	def final_update(self):
		cipher = self.trans_data.get()
		mac = self.trans_data.get()

		result = self.req_post({"cmd": "CONFIRM", "params": {"cipher": cipher, "mac": mac}})
		params = result['params']

		print(result)



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
#			self.trans_factory_key,
			self.chip_side.get_reg_key,
			self.server_side.prcess_register,
			#self.chip_side.prcess_chip_authentication,
			#self.server_side.final_update,
		]

		None
	def set_sideclass(self):
		self.server_side = RegProcessServerSide(self)
		self.chip_side = ChipSide(self)

	def trans_company_no(self):
		self.trans_data.put(self.comm_figure.company_no)
		#self.trans_data.set(self.comm_figure.factory_key_id)

	# def trans_factory_key(self):
	# 	self.trans_data.put(self.comm_figure.factory_key_id)
	# 	#self.trans_data.set(self.comm_figure.factory_key_id)


class RegProcessWithWebServer(RegProcess):

	def set_sideclass(self):
		self.server_side = RegProcessServerSideWithWebServer(self)
		self.chip_side = ChipSide(self)




if __name__ == '__main__':
	RegProcess().run()
	#RegProcessWithWebServer().run()