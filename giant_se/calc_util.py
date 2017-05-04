from neolib import neolib
from neolib import crypto_util

def calc_sn( puf):
	return calc_code(puf, crypto_util.zerofill(8))


def calc_code(puf, random):
	#return crypto_util.sha256(puf + random + e_fuse)
	#e_fuse = ''
	return left_16_sha256(puf + random)

def left_16(org):
	return crypto_util.substr(org, 0, 16)

def left_16_sha256(org):
	return left_16(crypto_util.sha256(org))
def left_8_sha256(org):
	return crypto_util.substr(crypto_util.sha256(org), 0, 8)


def mod8bits_calc(org, hashed_value):
	bytes0 = neolib.HexString2ByteArray(hashed_value)
	bytes1 = neolib.HexString2ByteArray(org)
	if len(bytes0) !=  len(bytes1) :
		return None
	lenth = len(bytes0)
	new_value = b''

	for idx in range(lenth):
		b0 = bytes0[idx]
		b1 = bytes1[idx]
		new_value+= bytes([(b0+b1)%256])
		idx += 1

	return neolib.ByteArray2HexString(new_value)


if __name__ == '__main__':
	#RegProcess().run()
	#print(mod8bits_calc('86E73517C718B6BB52D5E612A3F7D4C0', '9876B26C0E30315FFFCA6A558506DCAC'))
	print(calc_code('6B534B5A548A1E3EEF8F053B02AD7EF8','216EDE464B501E01334C72E0EA7F2FF3'))