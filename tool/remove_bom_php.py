import os
import neolib.neolib as neolib
import re
import codecs
BUFSIZE = 4096
BOMLEN = len(codecs.BOM_UTF8)

def find_files(base_path):

	for path, dirs, files in os.walk(base_path):

		for tmpfile in files:
			if ".php" in tmpfile:
				if base_path+'\\'+'wordpress' in path:
					continue
				allpath = path + "\\" + tmpfile
				with open(allpath, "r+b") as fp:
					chunk = fp.read(BUFSIZE)
					if chunk.startswith(codecs.BOM_UTF8):
						#print(allpath)
						yield allpath
					fp.close()


				dstfile = path + "\\" + re.sub(r'(\w+)\.diag', r'\1.png', tmpfile)

				# continue
	#			str = neolib.StrFromFile(allpath)



if __name__ == '__main__':
	ret = find_files(r'C:\APP\Bitnami\xampp\htdocs')
	#lists = list(ret)
	#print(lists)
	for tmp in ret:
		str= neolib.StrFromFile(tmp)
		nebytes = str.encode().replace(codecs.BOM_UTF8,b'')
		print(nebytes[0:10])
		print(str.encode()[0:10])
		neolib.StrToFile(nebytes.decode(),tmp)
		#str.startswith(codecs.BOM_UTF8)
		#print(neolib.Text2HexString(str[0:10]))

