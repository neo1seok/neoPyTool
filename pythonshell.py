import sys
import neolib
import win32api
import win32gui

import time
import re

from datetime import date





def GetFileNameOrg(str):
    return str

def GetFileNameByQutoType(str):
    return re.sub(r'\\',r'\\\\\\',str)




def getMap(list):
    
    return []


mapfunction = {"literal":lambda x:re.sub(r'\\',r'\\\\',x) ,
               "linux": lambda x: re.sub(r'\\', r'/', x),
               "org": lambda x: x,
               }


if __name__ != '__main__':
    exit()




maparg = neolib.listarg2Map(sys.argv)

print(maparg)

pffile = GetFileNameOrg

try :
    value = maparg["path"]
except:
    value = ""

try:
    pffile = mapfunction[maparg["type"]]
except:
    pffile = mapfunction["org"]


dststr = pffile(value)

win32api.MessageBox(0,dststr,"NEOPYTHONSHELL")
neolib.SetClipBoard(dststr)
