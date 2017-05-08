import requests
import  neolib.neoutil as neolib
import simplejson as json
import time
def test_get():
	r = requests.get('http://neo1seok.pe.kr:8080/giant_se/reg.do?key=get')
	print(r.text)
	print(neolib.Text2HexString(r.text))

def test_templete(ssess,uri,data):
	r = ssess.post(uri, data=data)
	print(r.text, r.cookies)
	return r.text

def test_post(ssess,address='neo1seok.pe.kr'):
	uri_reg = 'http://{0}/giant_se/reg.do'.format(address)
	uri_auth = 'http://{0}/giant_se/auth.do'.format(address)
	jsonvalue_reg = {
		"cmd": "START_REG_SESSION",
		"params": {
			"sn": "4C471a000000000047",
			"factory_key_id": "EDB0",

		}

	}
	jsonvalue_auth = {
		"cmd": "START_AUTH_SESSION",
		"params": {
			"sn": "4C471a000000000047",
			"factory_key_id": "EDB0",

		}

	}


	for idx in range(2):
		test_templete(ssess,uri_reg,data={'json': json.dumps(jsonvalue_reg)})

		test_templete(ssess, uri_auth,  data={'json': json.dumps(jsonvalue_auth)})
		# # r = ssess.post(uri, data={'json': json.dumps(jsonvalue_reg)})
		# # print(r.text, r.cookies)
		#
		#
		# r = ssess.post(uri, data={'json': json.dumps(jsonvalue_auth)})
		# print(r.text, r.cookies)


def test_post_giant_auth(ssess,address='neo1seok.pe.kr'):

	r = ssess.post('http://{0}:8080/giant_auth'.format(address), data={})
	print(r.text, r.cookies)

def test_post_giant_nfc(ssess, address='neo1seok.pe.kr'):
	uri = 'http://{0}/giant_nfc/NFC'.format(address)
	jsonvalue_auth ={
		"cmd": "REQ_SESSION",
		"params": {
			"sn": "4C471a000000000047",
			"factory_key_id": "EDB0",

		}

	}

	curtime = time.clock()
	ret_text = test_templete(ssess, uri, data={'cmd':'CMDBYJSON_ROW',"jsonbase64":json.dumps(jsonvalue_auth)})
	# r = ssess.post(uri, data={'cmd':'CMDBYJSON_ROW',"jsonbase64":json.dumps(jsonvalue_auth)})
	# print(r.text)
	retjson = json.loads(ret_text)
	uid = retjson['mapvValue']["UID"]

	jsonvalue_auth = {
		"cmd": "REQ_RAND",
		"params": {
			"UID": uid,
		}

	}
	ret_text = test_templete(ssess, uri,  data={'cmd': 'CMDBYJSON_ROW', "jsonbase64": json.dumps(jsonvalue_auth)})
	#r = ssess.post(uri,   data={'cmd': 'CMDBYJSON_ROW', "jsonbase64": json.dumps(jsonvalue_auth)})

	print(ret_text)
	tktime = time.clock()-curtime



def test_post_admin():
	jsonvalue = {
		"cmd":"LIST_CHIP",
		"params": {
			"sn":"4C471a000000000047",

		},
		'list_param':[
			{"sn":"4C471a000000000047"},
			{"sn": "4C471a000000000047" },
		],
		"crc16":""


	}
	r = requests.post('http://neo1seok.pe.kr:8080/giant_se/admin.do', data = {'json':json.dumps(jsonvalue)})
	print(r.text)
#test_post_session()
r = requests.get('http://neo1seok.pe.kr:8000')
print(r.text,r)

exit()
for _ in range(100):
	ssess = requests
	ssess = requests.session()
	test_post_giant_nfc(ssess, "dev.ictk.com")
	#test_post_giant_auth(ssess, "dev.ictk.com")
	test_post(ssess,"dev.ictk.com")
	ssess.close()


#test_post(ssess)
#test_post_giant_auth(ssess,"dev.ictk.com")
#

#test_post_giant2Auth(ssess,"dev.ictk.com")
