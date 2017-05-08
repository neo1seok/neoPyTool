from giant_se.calc_util import *
import simplejson as json
from  giant_se.reg_process import *
from  giant_se.auth_process import *
import queue
import  threading
import collections
import re
from concurrent.futures import ThreadPoolExecutor

def generate_puf(count):
	list_puf = []
	for idx in range(count):
		puf = crypto_util.getrandom(16)
		list_puf.append([puf, calc_sn(puf)])

	neoutil.StrToFile(neoutil.json_pretty(list_puf), 'rsc/pufs.json')

def load_pufs():
	sfdafas = neoutil.StrFromFile('rsc/pufs.json')
	return json.loads(sfdafas)
#
# def register_pufs():
# 	list_puf = load_pufs()
# 	for puf,sn in list_puf:
# 		RegProcessWithWebServer().set_puf(puf).run()

class ToolClass():
	def	__init__(self,process_obj,puf,logger,idx,address='localhost'):
		threading.Thread.__init__(self)

		self.puf = puf
		self.logger = logger
		self.idx = idx
		self.process_obj = process_obj
		self.address = address

	def run(self):
		print(self.idx,"start")
		#AuthProcessWithWebServer(self.logger).set_puf(self.puf).run()
		self.process_obj(self.logger).set_address(self.address).set_puf(self.puf).run()
		print(self.idx, "end")





def tesf_template(que_puf,process_obj,thread_count,address='localhost'):


	handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
	logger = neoutil.create_logger("tool", handler=handler)
	count = 0

	list_submit = []
	#que_puf = queue.Queue()
	with ThreadPoolExecutor(max_workers=thread_count) as e:
		while que_puf.qsize()>0:
			puf = que_puf.get()
			#for puf, sn in list_puf:
			toolclass = ToolClass(process_obj, puf, logger, count,address)
			submit = e.submit(toolclass.run)
			list_submit.append(submit)
			count += 1


def register_pufs(address='localhost'):
	list_puf = load_pufs()
	print(len(list_puf))
	que_puf = queue.Queue()
	[que_puf.put(puf) for puf, sn in list_puf]
	print(que_puf.qsize())
	#[ que_puf.put(puf) for puf, sn in list_puf]

	tesf_template(que_puf,RegProcessWithWebServer,100,address)
	# list_puf = load_pufs()
	# print(len(list_puf))
	# handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
	# logger = neolib.create_logger("tool", handler=handler)
	# count = 0
	#
	# list_threads = []
	# with ThreadPoolExecutor(max_workers=50) as e:
	# 	for puf, sn in list_puf:
	# 		thread = RegisterThreadClass(puf, logger, count)
	# 		submit = e.submit(thread.run)
	# 		list_threads.append(submit)
	# 		count+=1
	#


def authentication_pufs(count,address='localhost'):
	list_puf = load_pufs()
	print(len(list_puf))
	que_puf = queue.Queue()
	for tmpidx in range(count):
		idx = random.randrange(len(list_puf))
		print("idx:",idx)
		puf, sn = list_puf[idx]
		que_puf.put(puf)

	tesf_template(que_puf, AuthProcessWithWebServer, 100,address)

	#
	# list_puf = load_pufs()
	# #count = 0
	# handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
	# logger = neolib.create_logger("tool", handler=handler)
	# for tmpidx in range(count):
	# 	idx = random.randrange(len(list_puf))
	# 	print("idx:",idx)
	# 	puf, sn = list_puf[idx]
	# 	thread = ThreadClass(puf,logger)
	# 	thread.start()
	# 	#AuthProcessWithWebServer().set_puf(puf).run()
	# 	#count += 1


def authentication_pufs_sync(count):
	list_puf = load_pufs()
	#count = 0
	for idx in range(count):
		#idx = random.randrange(len(list_puf))
		print("idx:",idx)
		puf, sn = list_puf[idx]
		AuthProcessWithWebServer().set_puf(puf).run()
		count += 1

	print(count)


def single_test(address='localhost'):
	RegProcessWithWebServer().set_address(address).run()
	AuthProcessWithWebServer().set_address(address).run()

def make_input_form_json():
	strres = neoutil.StrFromFile('rsc/input_info.txt')
	mapobj = map(lambda x: tuple(x.split('\t')), strres.split('\r\n'))
	result = collections.OrderedDict()
	for row in mapobj:
		#print(len(row))
		if len(row) == 1: continue
		group_name,id,lable,type = row
		if group_name not in result:
			result[group_name] = collections.OrderedDict()
			result[group_name]['inputs'] = []

		if type == 'button':
			result[group_name]['button'] = {'lable':lable,'id':id }
			continue

		result[group_name]['inputs'].append({'lable':lable,'id':id })

	orgstr = neoutil.json_pretty(result)
	dst = re.sub(r'"(\w+)":',r'\1:',orgstr)

	print(dst)
def make_asciisn_map():
	ref = "0123456789ABCDEF"
	ref2 = "abcdefghijklmnopq"
	idx = 0
	ret =collections.OrderedDict()
	ret2 =collections.OrderedDict()
	for tmp in ref:
		ret[tmp] = ref2[idx]
		ret2[ref2[idx] ] = tmp
		idx +=1

	for ch1,ch2 in ret.items():
		aaa = "put('{0}','{1}');".format(ch1,ch2)
		print(aaa)
	print()
	for ch1,ch2 in ret2.items():
		aaa = "put('{0}','{1}');".format(ch1,ch2)
		print(aaa)
	return  ret,ret2
ret,ret2 = make_asciisn_map()

# print(neolib.json_pretty(ret))
# print(neolib.json_pretty(ret2))
exit()
#make_input_form_json()
#single_test('dev.ictk.com')
#register_pufs('dev.ictk.com')

authentication_pufs(1000,'dev.ictk.com')
print("end")
#authentication_pufs_sync(10)
exit()



