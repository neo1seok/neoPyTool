from neolib import neolib
from neolib import crypto_util

def calc_sn( puf, e_fuse):
	return calc_code(puf, crypto_util.zerofill(8), e_fuse)


def calc_code(puf, random, e_fuse):
	#return crypto_util.sha256(puf + random + e_fuse)
	e_fuse = ''
	return left_16_sha256(puf + random+e_fuse)

def left_16(org):
	return crypto_util.substr(org, 0, 16)

def left_16_sha256(org):
	return crypto_util.substr(crypto_util.sha256(org), 0, 16)


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