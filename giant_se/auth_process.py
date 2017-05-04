from giant_se.base_classes import *
from giant_se.chip_side import *



class AuthProcessServerSide(BaseServerSide):
	def prcess_random_values(self):
		sn = self.trans_data.get()
		self.extract_map_auth_info_from_sn(sn)
		self.RandomS = crypto_util.getrandom(16)

		random = self.auth_info.random
		random_server = self.RandomS
		self.print_view(locals(), 'sn')
		self.print_view(locals(), 'random')
		self.print_view(locals(), 'random_server')

		self.trans_data.put(self.auth_info.random)
		self.trans_data.put(self.RandomS)

		None

	def prcess_authentication(self):
		cipher = self.trans_data.get()
		mac = self.trans_data.get()

		hash_param, tRandom, newRandom, newAuthcode, calc_mac= self.calc_auth(self.auth_info.random ,self.auth_info.authcode,self.RandomS,cipher)

		self.print_view(locals(), 'hash_param')
		#self.print_view(locals(), 'tRandom_newAuthcode')
		self.print_view(locals(), 'tRandom')
		self.print_view(locals(), 'newRandom')
		self.print_view(locals(), 'newAuthcode')
		self.print_view(locals(), 'calc_mac')

		# self.print_view(locals(),'cipher')
		# self.print_view(locals(), 'mac')
		#
		# hash_param = crypto_util.sha256(self.auth_info.random + self.RandomS + self.auth_info.authcode)
		# self.print_view(locals(), 'hash_param')
		# tRandom_newAuthcode = crypto_util.xor_calc(cipher,hash_param)
		# self.print_view(locals(), 'tRandom_newAuthcode')
		# tRandom = crypto_util.substr(tRandom_newAuthcode, 0, 16)
		# newRandom = mod8bits_calc(tRandom,self.RandomS)
		# newAuthcode = crypto_util.substr(tRandom_newAuthcode, 16, 16)
		#
		# self.print_view(locals(), 'tRandom')
		# self.print_view(locals(), 'newRandom')
		# self.print_view(locals(), 'newAuthcode')
		#
		# self.auth_info.random = newRandom
		# self.auth_info.authcode = newAuthcode
		#
		#
		# calc_mac = left_16_sha256(newAuthcode + self.RandomS + tRandom)
		# self.print_view(locals(), 'calc_mac')






		if mac != calc_mac :
			raise Exception('result is differnet')
		self.server_figure.map_auth_info[self.auth_info.sn] = self.auth_info.get_dict()
		self.main_class.write_json(self.main_class.server_json_file, self.server_figure)






		#self.trans_data.put(self.param)

class AuthProcessServerSideWithWebServer(BaseServerSideWithWebServer):
	sublet = 'auth'
	def prcess_random_values(self):
		sn = self.trans_data.get()

		result = self.req_post({"cmd": "RANDOM_VALUES", "params": {"sn": sn}})
		params = result['params']


		self.trans_data.put(params['random'])
		self.trans_data.put(params['random_server'])

		None

	def prcess_authentication(self):
		cipher = self.trans_data.get()
		mac = self.trans_data.get()
		result = self.req_post({"cmd": "AUTHENTICATION", "params": {"cipher": cipher,"mac": mac}})
		print(result)




class AuthProcess(BaseProcess):
	def init(self):
		BaseProcess.init(self)
		self.set_sideclass()

		print("list_process count:",len(self.list_process))

		self.list_process.extend(  [
			self.chip_side.prcess_get_sn,
			self.server_side.prcess_random_values,
			self.chip_side.prcess_chip_authentication,
			self.server_side.prcess_authentication
		])

		None
	def set_sideclass(self):
		self.server_side = AuthProcessServerSide(self)
		#self.chip_side = AuthProcessChipSide(self)
		self.chip_side = ChipSide(self)




class AuthProcessWithWebServer(AuthProcess):

	def check_listcoutn(self):
		print("list_process count:", len(self.list_process))
	def set_sideclass(self):
		self.server_side = AuthProcessServerSideWithWebServer(self)
		#self.chip_side = AuthProcessChipSide(self)
		self.chip_side = ChipSide(self)




if __name__ == '__main__':
	AuthProcess().run()
	#AuthProcessWithWebServer().run()