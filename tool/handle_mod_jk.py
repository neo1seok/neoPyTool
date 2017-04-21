from tool.util import find_files
from shutil import copyfile

if __name__ == '__main__':
	def is_php_with_bomfile(tuplepath,etc_param):
		base_path,path, file = tuplepath
		if file != "mod_jk.so" :
			return False
		return True

	base_path = r'C:\Temp\mod_jk_module'
	ret = find_files(base_path,is_php_with_bomfile)
	dst_path = r"C:\app\bitnami\xampp\apache\modules"
	for base_path,path, file in ret:
		new_sub_path = path.replace(base_path+'\\tomcat-connectors-','')
		tmp = path + "\\" + file
		new_path = "{0}\\mod_jk_{1}.so".format(dst_path,new_sub_path)
		new_file = "mod_jk_{1}.so".format(dst_path, new_sub_path)
		#copyfile(tmp, new_path)


		print(new_file)
		continue


