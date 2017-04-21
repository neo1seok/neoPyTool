import os

def find_files(base_path,is_filter,etc_param=None):
	'''
	이 함수는 특정 패스 밑에 모든 파일을 리커시브하게 읽어가며
	디텍트 하는 함수이다.
	:param base_path:
	:return:
	'''

	for path, dirs, files in os.walk(base_path):

		for tmpfile in files:
			tuplepath = (base_path,path, tmpfile)
			if is_filter(tuplepath,etc_param):
				yield tuplepath

