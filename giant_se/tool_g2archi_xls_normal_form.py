from neolib import neoutil
import collections
strmenu = neoutil.StrFromFile('rsc/g2_archigecture.txt')
mapobj = map(lambda x: tuple(x.split('\t')), strmenu.split('\r\n'))
list_row = list(mapobj)
print(list_row)
map_calins = collections.OrderedDict()
cur_clains = ""
for tmp in list_row:
	length = len(tmp)
	if length != 10:
		tmp = list(tmp)
		extend_rest = ["" for _ in range(10 - length)]
		print(extend_rest)
		tmp.extend(extend_rest)
	Command, CLA, INS, P1, P2, Lc, Data, Le, DATA, SW = ("","","","","","","","","","",)
	try:
		Command, CLA, INS, P1, P2, Lc, Data, Le, DATA, SW = tmp
	except:
		Command = tmp[0]
	if "".join(tmp) == '':
		continue

	clains = CLA + INS
	cur_clains = clains if clains != '' else cur_clains

	if cur_clains not in map_calins:
		map_calins[cur_clains] =[]
	map_calins[cur_clains].append((Command, CLA, INS, P1, P2, Lc, Data, Le, DATA, SW,))
	print(cur_clains,tmp)
neoutil.StrToFile(neoutil.json_pretty(map_calins), "sample_xml.txt")

list_final =[]
def funtion(sumstr,str):
	endline = " "
	# if str !="":
	# 	endline = '\n'

	return sumstr + endline+str
for key,value in 	map_calins.items():
	sumCommand, sumCLA, sumINS, sumP1, sumP2, sumLc, sumData, sumLe, sumDATA, sumSW = ("", "", "", "", "", "", "", "", "", "",)
	for row in value :
		Command, CLA, INS, P1, P2, Lc, Data, Le, DATA, SW =row

		sumCommand = funtion(sumCommand, Command)
		sumCLA = funtion(sumCLA, CLA)
		sumINS = funtion(sumINS, INS)
		sumP1 = funtion(sumP1, P1)
		sumP2 = funtion(sumP2, P2)
		sumLc = funtion(sumLc, Lc)
		sumData = funtion(sumData, Data)
		sumLe = funtion(sumLe, Le)
		sumDATA = funtion(sumDATA, DATA)
		sumSW = funtion(sumSW, SW)

		None
	list_final.append((sumCommand, sumCLA, sumINS, sumP1, sumP2, sumLc, sumData, sumLe, sumDATA, sumSW,))
	[list_final.append(("", "", "", "", "", "", "", "", "", "",)) for _ in range(len(value) -1)]


outstr =""
for row in list_final:
	outstr +="\t".join(row) +"\n"
neoutil.StrToFile(outstr, "out2.txt")
print(map_calins)
#print(list(mapobj))