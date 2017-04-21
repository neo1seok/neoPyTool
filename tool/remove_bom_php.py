import os
import neolib.neolib as neolib
import re
import codecs
from tool.util import find_files

BUFSIZE = 4096
BOMLEN = len(codecs.BOM_UTF8)




if __name__ == '__main__':
	def is_php_with_bomfile(tuplepath,etc_param):
		base_path,path, file = tuplepath
		if ".php" not in file:
			return False
		if base_path + '\\' + 'wordpress' in path:
			return False
		return True

		allpath = path + "\\" + file
		with open(allpath, "r+b") as fp:
			chunk = fp.read(BUFSIZE)
			if chunk.startswith(codecs.BOM_UTF8):
				# print(allpath)
				return True
			fp.close()
		return False


	base_path = r'C:\APP\Bitnami\xampp\htdocs'
	ret = find_files(base_path,is_php_with_bomfile)
	#lists = list(ret)
	#print(lists)
	for base_path,path, tmpfile in ret:
		tmp = path + "\\" + tmpfile
		print(tmp)
		continue
		str= neolib.StrFromFile(tmp)
		nebytes = str.encode().replace(codecs.BOM_UTF8,b'')
		print(nebytes[0:10])
		print(str.encode()[0:10])
		#neolib.StrToFile(nebytes.decode(),tmp)
		#str.startswith(codecs.BOM_UTF8)
		#print(neolib.Text2HexString(str[0:10]))

