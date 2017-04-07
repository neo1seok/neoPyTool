from giant_se.base_classes import *

class AuthProcessChipSide(BaseChipSide):
	def prcess_trans_cipher_mac_keys_client(self):
		Random = self.trans_data.get()
		RandomS = self.trans_data.get()
		Authcode = self.calc_authcode(Random)
		tRandom = crypto_util.getrandom(16)
		newRandom = mod8bits_calc(tRandom,RandomS)
		newAuthcode = self.calc_authcode(newRandom)
		hash_param = crypto_util.sha256(Random + RandomS+Authcode)
		cipher = crypto_util.xor_calc( tRandom+newAuthcode,hash_param)
		mac = left_16_sha256(newAuthcode+RandomS+tRandom)
		self.trans_data.put(cipher)
		self.trans_data.put(mac)



class AuthProcessServerSide(BaseServerSide):
	def prcess_trans_random_keys_server(self):
		sn = self.trans_data.get()
		self.extract_map_auth_info_from_sn(sn)


		self.RandomS = crypto_util.getrandom(16)
		self.trans_data.put(self.auth_info.random)
		self.trans_data.put(self.RandomS)

		None


	def prcess_auth_server(self):
		cipher = self.trans_data.get()
		mac = self.trans_data.get()
		self.print_view(locals(),'cipher')
		self.print_view(locals(), 'mac')

		hash_param = crypto_util.sha256(self.auth_info.random + self.RandomS + self.auth_info.authcode)
		self.print_view(locals(), 'hash_param')
		tRandom_newAuthcode = crypto_util.xor_calc(cipher,hash_param)
		self.print_view(locals(), 'tRandom_newAuthcode')
		tRandom = crypto_util.substr(tRandom_newAuthcode, 0, 16)
		newRandom = mod8bits_calc(tRandom,self.RandomS)
		newAuthcode = crypto_util.substr(tRandom_newAuthcode, 16, 16)

		self.print_view(locals(), 'tRandom')
		self.print_view(locals(), 'newRandom')
		self.print_view(locals(), 'newAuthcode')

		self.auth_info.random = newRandom
		self.auth_info.authcode = newAuthcode


		calc_mac = left_16_sha256(newAuthcode + self.RandomS + tRandom)
		self.print_view(locals(), 'calc_mac')






		if mac != calc_mac :
			raise Exception('result is differnet')
		self.server_figure.map_auth_info[self.auth_info.sn] = self.auth_info.get_dict()
		self.main_class.write_json(self.main_class.server_json_file, self.server_figure)






		#self.trans_data.put(self.param)

class AuthProcess(BaseProcess):
	def init(self):
		BaseProcess.init(self)
		self.server_side = AuthProcessServerSide(self)
		self.chip_side = AuthProcessChipSide (self)

		self.list_process.extend(  [
			self.chip_side.prcess_trans_sn,
			self.server_side.prcess_trans_random_keys_server,
			self.chip_side.prcess_trans_cipher_mac_keys_client,
			self.server_side.prcess_auth_server
		])

		None




if __name__ == '__main__':
	AuthProcess().run()