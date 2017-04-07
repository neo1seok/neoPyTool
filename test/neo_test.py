import neolib.crypto_util as crypto_util


if __name__ == '__main__':
	print("hexstr_sha_256", crypto_util.sha256('234455'))
	print("hexstr_substr", crypto_util.substr('234455', 0, 2))
	print("hexstr_zerofill", crypto_util.zerofill(10))

	print("hexstr_getrandom", crypto_util.getrandom(32))
	print("hexstr_getrandom", crypto_util.getrandom(10))
	print("hexstr_getrandom", crypto_util.getrandom(10))
	print("hexstr_getrandom", crypto_util.getrandom(10))

	print("xor_encrytp")
	org = '1BB05A46A8A17036C15349053E8CD29B00E019DDFCC6741B1B6FAFDBD6B7C4FE1BB05A46A8A17036C15349053E8CD29B00E019DDFCC6741B1B6FAFDBD6B7C4FE'
	calccode = 'DF2F43D70CD08203CACA5BE5093CD2B423DA14416BC76DCD0D9F9A2C730ED9EF'
	encodedcode = crypto_util.xor_calc(org, calccode)
	decodecode = crypto_util.xor_calc(encodedcode, calccode)
	print("org", org)
	print("calccode", calccode)
	print("encodedcode", encodedcode)
	print("decodecode", decodecode)