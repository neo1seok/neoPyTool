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


import neolib.neoutil as neolib


#import test.sample


import xlrd


class TestClass:

	aab = ''
	def test(self):
		None
	def test2(self):
		None
	def test3(self,a,c,d):
		None

	def Show(self,a,b,c):
		sig = inspect.signature(self.Show)
		print(str(sig))
		# args, _, _, values = inspect.getargvalues(frame)
		# print(args)
		# print(dir(self))
		# method_list = [func for func in dir(self) if callable(getattr(self, func))]
		# print(method_list)
		None

from urllib.parse import quote,unquote,quote_plus
#인코딩

def urlencode(string):
	print ("URLEncoding:",quote_plus(string))
#디코딩
def urldecode(string):
	print ("URLDecoding:",unquote(string))

urlencode("auth?json={%22cmd%22:%22REQ_START_SESSION%22,%22params%22:{%22sn%22:%224C4715000000000047%22}}")


import urllib.request
from Crypto.Hash import SHA256

#import winrandom
import sysconfig
print(sysconfig.get_config_vars())

exit()
str = neolib.StrFromFile('rsc/계좌.txt')
lines = str.split('\r\n')
listlist = [ [cols for cols in tmp.split('\t')  ] for tmp in str.split('\r\n') ]
newlistlist = []
for row  in listlist:
	if len(row) <= 1:continue
	if row[0] == '거래일자' or  row[4] == '0':continue

	if int(row[4]) < 1000000 :continue
	newlistlist.append(row)

newstr = "\r\n".join([ "\t".join(row) for row  in newlistlist])
print(newstr)
neolib.StrToFile(newstr,'rsc/계좌new.txt')
exit()
import Crypto.Hash
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import pyelliptic

iv = pyelliptic.Cipher.gen_IV('aes-256-cfb')
ctx = pyelliptic.Cipher("secretkey", iv, 1, ciphername='aes-256-cfb')

ciphertext = ctx.update('test1')
ciphertext += ctx.update('test2')
ciphertext += ctx.final()
print(ciphertext)
ctx2 = pyelliptic.Cipher("secretkey", iv, 0, ciphername='aes-256-cfb')
print(ctx2.ciphering(ciphertext))


# Asymmetric encryption
alice = pyelliptic.ECC() # default curve: sect283r1
bob = pyelliptic.ECC(curve='sect571r1')

ciphertext = alice.encrypt("Hello Bob", bob.get_pubkey(),
                           ephemcurve='sect571r1')
print(bob.decrypt(ciphertext))

signature = bob.sign("Hello Alice")
# alice's job :
print(pyelliptic.ECC(pubkey=bob.get_pubkey(),
                     curve='sect571r1').verify(signature, "Hello Alice"))


exit()

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
print(hex(key.key.n))
print(type(key.key.e))
print(key.key.d)


publickey = key.publickey() # pub key export for exchange

print(publickey)
encrypted = publickey.encrypt('encrypt this message'.encode(), 32)
print(encrypted)
#message to encrypt is in the above line 'encrypt this message'

print( 'encrypted message:', encrypted) #ciphertext

f = open ('encryption.txt', 'w')
f.write(str(encrypted)) #write ciphertext to file
f.close()

#decrypted code below

f = open('encryption.txt', 'r')
message = f.read()


decrypted = key.decrypt(ast.literal_eval(str(encrypted)))

print( 'decrypted', decrypted)

f = open ('encryption.txt', 'w')
f.write(str(message))
f.write(str(decrypted))
f.close()
exit()
hash = Crypto.Hash.SHA256.new()

hash.update("Nobody inspects".encode())
hash.update(" the spammish repetition".encode())

print(neolib.ByteArray2HexString(hash.digest()))
m = hashlib.sha256()
m.update("Nobody inspects".encode())
m.update(" the spammish repetition".encode())

print(neolib.ByteArray2HexString(m.digest()))

from Crypto.Cipher import AES

obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
message = "The answer is no"

ciphertext = obj.encrypt(message)

print(neolib.ByteArray2HexString(ciphertext))


obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
print(obj2.decrypt(ciphertext).decode())




exit()
import ctypes
Win32DLL = ctypes.WinDLL("D:/PROJECT/ADVANCE/Win32DLL/x64/Debug/Win32DLL.dll")
Win32DLL.fnWin32DLL()

exit()
print(re.match(r'asdsa',"adsaf"))

print( globals()['TestClass'])

TestClass().Show(1,2,3)

exit()

print(int('ff', 16))

exit()
klass = globals()["Test"]
instance = klass()
r = requests.get("http://purryfwends.com/article/240/Graphic/warning-graphic-content-naked-man-attempts-suicide-by-lion-cage-turtle-chopped-in-half-revenge-bites-man-compilation")
print(r.text)

import logging
from logging import handlers





handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')


# create logger
logger = logging.getLogger('show369')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
handler.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(handler)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')

import test.sample
print(b'aabb')
exit()
