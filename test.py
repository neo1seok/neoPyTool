import base64
import glob
import gzip
import hashlib
import http.client
import os
import re
import shutil
import socket
import sys

import win32api
import inspect
import requests
import  simplejson as json
import win32gui
import win32con
import time
import datetime
from datetime import date
import threading
import neolib.neolib4Win as neolib4Win
from  math import cos,sin,pi
import pickle
import subprocess
import neolib.neoserver


neolib.neoserver.HandleServerWithLogging(5510,neolib.neoserver.SampleEchoHandleClient).run()

exit()
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
time.sleep(1)
print('테스트')
proc = subprocess.Popen('python C:/app/neoPyTool/test/test_kbd_mouse_event.py', startupinfo=startupinfo)
#proc = subprocess.Popen('dir',  creationflags=subprocess.SW_HIDE, shell=True)
proc.wait()

exit()
from smartcard.scard import *
import smartcard.util

import neolib.neolib as neolib
from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRC32 import CRC32
from PyCRC.CRCCCITT import CRCCCITT

import ntplib
from time import ctime
import neotool
import pytz, datetime
import traceback
# local = pytz.timezone ("Asia/Seoul")
# naive = datetime.datetime.now()
# local_dt = local.localize(naive, is_dst=None)
# utc_dt = local_dt.astimezone (pytz.utc)
# print(utc_dt)
# print(naive)
#
# print('test')
#neotool.UpdaateSystemTime(neolib.listarg2Map(sys.argv)).Test()
#exit()
import blockdiag


from blockdiag import parser, builder, drawer

#str = neolib.StrFromFile('C:/TMP/diagrams/background_url_image.diag')


bytes = neolib.HexString2ByteArray("102300")
print(",".join('{:02X}'.format(x) for x in bytes))

exit()
for path,dirs,files in os.walk('C:/TMP/diagrams'):
	for tmpfile in files :
		if ".diag" in tmpfile:
			allpath = path+"\\"+tmpfile
			dstfile = path+"\\"+re.sub(r'(\w+)\.diag',r'\1.png',tmpfile)
			print(dstfile)
			#continue
			str = neolib.StrFromFile(allpath)
			tree = parser.parse_string(str)
			diagram = builder.ScreenNodeBuilder.build(tree)
			draw = drawer.DiagramDraw('PNG', diagram, filename=dstfile)
			draw.draw()
			draw.save()


bytes = neolib.HexString2ByteArray("102300")
",".join('{:02X}'.format(ord(x)) for x in bytes)

exit()
import binascii

ber = (
"\x63\x04hell"                  # simple tag, len
"\x64\x04hell"                  # test read length
"\x1f\x81\x82\x82\x04\x00"      # extended tag
"\x65\x81\x01!"                 # extended len
"\x65\x83\x00\x00\x04!..!"      # mroe extended len
)
seq = (b for b in ber)
print(type(seq))
print(seq)
print(next(seq))
print(next(seq))
rv = dict()

tag = ber[0]
print(tag,type(tag))
tag += ber[1]
print(tag,type(tag))
import pprint
pprint.pprint(rv)
exit()
from shutil import copytree, ignore_patterns
def copy_user(src, dst, *, follow_symlinks=True):
	print(dst)
	shutil.copy2(src, dst)

copytree('C:\APP\PYTOOL', 'C:\Temp\copy_test', copy_function=copy_user,ignore=ignore_patterns('*.pyc', 'tmp*'))

exit()

def do_oth(instnace):
	while True:
		instnace.othre_trhread()

	None

class MapTest:
	def __init__(self):
		self.maptest = {}

	def	run(self):

		self.view()

	def othre_trhread(self):
		self.maptest['23'] = 3
		self.view()


	def view(self):
		print(self.maptest)

instnace = MapTest()
instnace.run()

thread1 = threading.Thread(target=do_oth,args=(instnace,))
thread1.start()

while True:
	time.sleep(1)

exit()
nonce = b'\x00' * 32
ENCRYPT_MODE_MASK = 0x81
inv= ~ENCRYPT_MODE_MASK
mode = 9

print(bin(ENCRYPT_MODE_MASK),bin(inv),ENCRYPT_MODE_MASK,inv)
print((mode & ~ENCRYPT_MODE_MASK != 0))
exit()
#nonce[0:8] = b'\x11'
#nonce[12:12+4] = b'\x11'*12



print([tmp for tmp in nonce ])

exit()
#import test.sample
def il005_calculate_crc16(length,data):

	crc16_register = 0
	polynomial = 0x8005  # polynomial : 0x8005
	crc16 = [0]*2
	for counter in range(length):
		shift_register = 0x01
		for shift_pos in range(8):
			data_bit = 1 if (data[counter] & shift_register) else 0
			shift_register <<= 1
			crc16_bit = crc16_register >> 15;
			crc16_register <<= 1;
			if (data_bit ^ crc16_bit) != 0 :
				crc16_register ^= polynomial;

	crc16[0] = crc16_register;
	crc16[1] = crc16_register >> 8;

	return crc16

#buff = neolib.HexString2ByteArray('234547DC03000000000000000047550100C80055008F8080A182E0A3609440A085')
buff = b'#EG\xdc\x03\x00\x00\x00\x00\x00\x00\x00\x00GU\x01\x00\xc8\x00U\x00\x8f\x80\x80\xa1\x82\xe0\xa3`\x94@\xa0\x85'

print(buff,buff[0])
def revbits(x,numbits):
	rev = 0
	for i in range(numbits):
		rev <<= 1
		rev += x & 1
		x >>= 1
	return rev

def revbitsperbytes(buff):
	retbuff = []
	for byte in buff:
		retbuff.append(revbits(byte,8))
	return bytes(retbuff)

input = b'\x05d\x05\xc0\x00\x01\x00\x0c'

output = revbitsperbytes(input)
print(input,neolib.ByteArray2HexString(output))
rescrc = CRC16().calculate(buff)
rvrsbyte = revbitsperbytes(rescrc.to_bytes(2,byteorder='big'))
print(neolib.ByteArray2HexString(rvrsbyte))
print(buff,hex(rescrc),bin(rescrc),hex(revbits(rescrc,16)),bin(revbits(rescrc,16)))

ret = il005_calculate_crc16(33,buff)
print(ret)

exit()

import xlrd
def accept_plus(s):
	if s <0 :return 0
	return s


pos = win32gui.GetCursorPos()
print(pos)

#points = [pos,(pos[0]-100,pos[1]-100),(pos[0]-100,pos[1]+100),(pos[0]+100,pos[1]+100),(pos[0]+100,pos[1]-100)]
points=[]
r = 100;
unitrad = 2*pi/100.0

for idx in range(100):
	rad = idx* unitrad
	posunit =(int(accept_plus(r*cos(rad)+pos[0])),int(accept_plus(r*sin(rad)+pos[1])))
	points.append(posunit)




dc = win32gui.GetDC(None)
hpen = win32gui.CreatePen(win32con.PS_SOLID, 3 , win32api.RGB(255, 0 , 0 ) )
horg = win32gui.SelectObject(dc,hpen)
win32gui.Polyline(dc,points)
win32gui.SelectObject(dc,horg)
win32gui.DeleteObject(hpen)
win32gui.ReleaseDC(None,dc)

time.sleep(1)
win32gui.InvalidateRect(None,None,True)


#os.system ('bash')