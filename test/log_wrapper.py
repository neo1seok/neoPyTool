import logging
from logging import handlers
import inspect

class NeoLogWrapper():
	def __init__(self,title):
		self.handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
		self.logger = self.createLogger(title, self.handler)

	def createLogger(self,loggename,handler):

		#handler = handlers.TimedRotatingFileHandler(filename=loggename + ".txt", when='D')
		self.loggename = loggename
		# create logger
		self.logger = logging.getLogger(loggename)
		self.logger.setLevel(logging.DEBUG)

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# create formatter
		formatter = logging.Formatter('%(asctime)s - %(name)s -%(pathname)s -%(lineno)s  %(levelname)s - %(message)s')

		# add formatter to ch
		ch.setFormatter(formatter)
		handler.setFormatter(formatter)
		# add ch to logger
		self.logger.addHandler(ch)
		self.logger.addHandler(handler)
		return self.logger

	def debug(self,str):
		frame = inspect.currentframe()
		print(dir(frame))
		print()
		print("f_back",frame.f_back)
		print("f_builtins",frame.f_builtins)
		print("f_code",frame.f_code)
		print("f_globals",frame.f_globals)
		print("f_lasti",frame.f_lasti)
		print("f_lineno",frame.f_lineno)
		print("f_locals",frame.f_locals)
		print("f_trace",frame.f_trace)


		print()
		for tmp in traceback.extract_stack():
			print(tmp.filename)
			print("name:", tmp.name)
			print("locals:", tmp.locals)
			print("lineno:", tmp.lineno)
			print("filename:", tmp.filename)

		self.logger.debug(str)

def safdafds():

	print(traceback.print_stack())
	#fasdfdf = traceback.FrameSummary()

	#for tmp in traceback.extract_stack():


def safdafds2():
	safdafds()
	#print(traceback.extract_stack())

if __name__ == '__main__':
	import traceback
	print(dir(traceback.FrameSummary))
	#print(traceback.extract_stack())

	#safdafds2()
	afsafsa = NeoLogWrapper("asfdaf")
	afsafsa.debug("TEST")