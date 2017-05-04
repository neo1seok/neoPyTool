from giant_se.base_classes import *

class ChipSide(BaseChipSide):
	def get_reg_key(self):
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


		FactoryKey = left_16_sha256(factorykeyid + self.chip_figure.factory_key_rtl)
		hash_param = crypto_util.sha256(Nonce + FactoryKey)
		Random_Authcode = Random+Authcode
		self.print_view(locals(), 'FactoryKey')
		self.print_view(locals(), 'hash_param')
		self.print_view(locals(), 'Random_Authcode')
		Cither = crypto_util.xor_calc(Random_Authcode, hash_param)
		mac = left_8_sha256(Random_Authcode)
		self.print_view(locals(), 'Cither')
		self.print_view(locals(), 'mac')

		self.trans_data.put(Nonce)
		self.trans_data.put(Cither)
		self.trans_data.put(mac)

	def prcess_chip_authentication(self):
		Random = self.trans_data.get()
		RandomS = self.trans_data.get()
		puf = self.chip_figure.puf
		Authcode = self.calc_authcode(Random)

		self.print_view(locals(), 'Random')
		self.print_view(locals(), 'RandomS')
		self.print_view(locals(), 'Authcode')
		self.print_view(locals(), 'puf')




		tRandom = crypto_util.getrandom(16)

		self.print_view(locals(), 'tRandom')

		newRandom = mod8bits_calc(tRandom,RandomS)
		self.print_view(locals(), 'newRandom')
		newAuthcode = self.calc_authcode(newRandom)
		self.print_view(locals(), 'newAuthcode')
		hash_param = crypto_util.sha256(Random + RandomS+Authcode)
		self.print_view(locals(), 'hash_param')
		cipher = crypto_util.xor_calc( tRandom+newAuthcode,hash_param)
		mac = left_16_sha256(newAuthcode+RandomS+tRandom)
		self.print_view(locals(), 'cipher')
		self.print_view(locals(), 'mac')
		self.trans_data.put(cipher)
		self.trans_data.put(mac)