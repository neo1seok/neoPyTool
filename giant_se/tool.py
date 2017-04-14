from giant_se.calc_util import *
import simplejson as json
from  giant_se.reg_process import *
from  giant_se.auth_process import *
import queue
import  threading
from concurrent.futures import ThreadPoolExecutor

def generate_puf(count):
	list_puf = []
	for idx in range(count):
		puf = crypto_util.getrandom(64)
		list_puf.append([puf, calc_sn(puf)])

	neolib.StrToFile(neolib.json_pretty(list_puf), 'rsc/pufs.json')

def load_pufs():
	sfdafas = neolib.StrFromFile('rsc/pufs.json')
	return json.loads(sfdafas)
#
# def register_pufs():
# 	list_puf = load_pufs()
# 	for puf,sn in list_puf:
# 		RegProcessWithWebServer().set_puf(puf).run()

class ToolClass():
	def	__init__(self,process_obj,puf,logger,idx):
		threading.Thread.__init__(self)

		self.puf = puf
		self.logger = logger
		self.idx = idx
		self.process_obj = process_obj

	def run(self):
		print(self.idx,"start")
		#AuthProcessWithWebServer(self.logger).set_puf(self.puf).run()
		self.process_obj(self.logger).set_puf(self.puf).run()
		print(self.idx, "end")





def tesf_template(que_puf,process_obj,thread_count):


	handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
	logger = neolib.create_logger("tool", handler=handler)
	count = 0

	list_submit = []
	#que_puf = queue.Queue()
	with ThreadPoolExecutor(max_workers=thread_count) as e:
		while que_puf.qsize()>0:
			puf = que_puf.get()
			#for puf, sn in list_puf:
			toolclass = ToolClass(process_obj, puf, logger, count)
			submit = e.submit(toolclass.run)
			list_submit.append(submit)
			count += 1


def register_pufs():
	list_puf = load_pufs()
	print(len(list_puf))
	que_puf = queue.Queue()
	[que_puf.put(puf) for puf, sn in list_puf]
	print(que_puf.qsize())
	#[ que_puf.put(puf) for puf, sn in list_puf]

	tesf_template(que_puf,RegProcessWithWebServer,100)
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


def authentication_pufs(count):
	list_puf = load_pufs()
	print(len(list_puf))
	que_puf = queue.Queue()
	for tmpidx in range(count):
		idx = random.randrange(len(list_puf))
		print("idx:",idx)
		puf, sn = list_puf[idx]
		que_puf.put(puf)

	tesf_template(que_puf, AuthProcessWithWebServer, 100)

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




#register_pufs()

authentication_pufs(100)
print("end")
#authentication_pufs_sync(10)
exit()



