import requests
import  neolib.neolib as neolib
import simplejson as json
def test_get():
	r = requests.get('http://neo1seok.pe.kr:8080/giant_se/reg.do?key=get')
	print(r.text)
	print(neolib.Text2HexString(r.text))
def test_post(ssess,address='neo1seok.pe.kr'):
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
		r = ssess.post('http://{0}:8080/giant_se/reg.do'.format(address), data={'json': json.dumps(jsonvalue_reg)})
		print(r.text, r.cookies)


		r = ssess.post('http://{0}:8080/giant_se/auth.do'.format(address), data={'json': json.dumps(jsonvalue_auth)})
		print(r.text, r.cookies)



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
ssess = requests
ssess = requests.session()
#test_post(ssess,"dev.ictk.com")
test_post(ssess)