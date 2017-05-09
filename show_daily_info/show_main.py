import re
import requests
import datetime
import shutil
import sys
import time
import gc
import  json
import time
import codecs
import base64
import logging
import collections
from logging import handlers
import neolib.neoutil as neolib

import hashlib
from show_daily_info.base_client import *

from show_daily_info.show_goldfish import HTTPCLientGoldFish
from show_daily_info.show_naverweb import GetLateestWebtoon









class LoopProcess(BaseClient):
	waittime = 20
	takentime = 1
	maxtime = 1;
	unittime = 10;
	version = 1.0

	def __init__(self,waittime,unittime):
		super(LoopProcess, self).__init__('LoopProcess')

		self.waittime = waittime
		self.unittime =unittime
		self.logger.info("LoopProcess waittime:{0} min VER:{1}".format(waittime,self.version))


	def getCurTime(self):
		return time.time()
	def doRun(self):

		self.maxtime = self.waittime * 60
		self.takentime = self.maxtime+1
		#handle369 = HTTPCLient369(self.handler)
		handleGoldFish = HTTPCLientGoldFish(self.handler)
		handleebtoon = GetLateestWebtoon(self.handler)

		listHandler = [handleGoldFish,handleebtoon]
		start = -1*self.maxtime;
		while True:

			self.takentime = self.getCurTime() - start;
			#self.logger.debug("%d %d %d",self.getCurTime(),self.takentime,start)
			self.logger.debug("LOOP VER:{2} tktime:{0} {1} ".format(self.takentime, self.maxtime,self.version))

			if self.takentime > self.maxtime:
				start = self.getCurTime()
				for tmp in listHandler:
					try:
						self.logger.info("RUN CLASSNAME:{0} ".format(tmp.__class__))
						tmp.Run();
					except:
						self.logger.debug("{0}  ValueError:{1}  \n".format(tmp.__name__,0))
				continue

			time.sleep(self.unittime)



if __name__ != '__main__':
	exit()
maparg = neolib.getMapsFromArgs(sys.argv)
#GetLateestWebtoon().doRun_test()
#exit()


waittime = 0.1
takentime = 1
maxtime = 1;
unittime = 10;
isAll = 'false'
print(maparg.keys())
if 'waittime' in maparg.keys() :
	waittime = int(maparg['waittime'])

if 'unittime' in maparg.keys() :
	unittime = int(maparg['unittime'])



LoopProcess(waittime,unittime).Run()
#HTTPCLient369().doRun()
#exit()



log = ''






