import requests
import  neolib.neolib as neolib
import simplejson as json
def test_get():
	r = requests.get('http://neo1seok.pe.kr:8080/giant_se/auth.do?key=get')
	print(r.text)
	print(neolib.Text2HexString(r.text))
def test_post():
	jsonvalue = {
		"cmd":"REQ_START_SESSION",
		"params": {
			"sn":"4C471a000000000047"

		},
		"crc16":""


	}
	r = requests.post('http://neo1seok.pe.kr:8080/giant_se/auth.do', data = {'json':json.dumps(jsonvalue)})
	print(r.text)
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
test_post_admin()