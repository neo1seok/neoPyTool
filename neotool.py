from neotool.neotool_class import *


if __name__ != '__main__':
	exit()

maparg = neolib.listarg2Map(sys.argv)
cmd = maparg["rt"]
main_process(cmd,maparg)
	#
	# mapfunction = {"strcpy": SetClipBoard,
	# 			   "conv2java": ConvertMapCs2Java,
	# 			   "makeNormalTxt": MakeNormalTxtInClipBoard,
	# 			   "convuplow": ConvUpperLowInClipBoard,
	# 			   "convdeftype": ConvDefineStringClipBoard,
	# 			   "puttyrun": PuttyRunNMove,
	# 			   "puttykill": PuttyKIll,
	# 			   "drawMousePos": drawMousePos,
	# 			   "UpdateSystemTime": UpdateSystemTime
	# 			   }
	#
	# cmd = maparg["rt"]
	# print(maparg)
	# runobj = mapfunction[cmd](maparg)
	# runobj.doRun()
	# time.sleep(0.5)  # delays for 5 seconds
	# exit()
	# i = 5
	# while i > 0:
	# 	time.sleep(1)  # delays for 5 seconds
	# 	print(str(i) + "second left")
	# 	i -= 1





