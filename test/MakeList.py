import os
import re
import shutil
import win32api
import glob


basepath = 'D:\\PROJECT\\스마트로\\TEMP\\SMARTRO_new3\\SMARTRO\\bin'

fp = open("sample_xml.txt","w")
for file in glob.glob(basepath  + '\\*.*'):
    print(file)
    fp.writelines(file)

fp.close()