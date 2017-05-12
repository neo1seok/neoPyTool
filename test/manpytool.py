import  sys
import datetime
import time
import os

if __name__ != '__main__':
	exit()

waittime = 20

if len(sys.argv) > 1:
	waittime = int(sys.argv[1])
	print(waittime)


takentime = waittime * 60+1;
unittile = 10;

while True:

	if takentime> waittime * 60:
		log = "{0} tktime:{1} doRun \n".format(datetime.datetime.now().isoformat(), 0)

		takentime = 0

	print(log);
	f = open("sample_xml.log", 'ab')
	f.write(log.encode())
	f.close()

	time.sleep(unittile)
	takentime += unittile;
	log = "{0} tktime:{1} \n".format(datetime.datetime.now().isoformat(), takentime)