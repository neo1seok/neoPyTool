import neolib.neoutil as neolib
import re
import collections

import datetime
from datetime import date, timedelta


def get_twice_mapinfo():

	orgstr = neolib.StrFromFile("rsc/twice.txt")
	result = []
	mapline = None  # collections.OrderedDict()

	for line in orgstr.split("\r\n"):

		comps = line.split(":")
		if len(comps) == 1:
			if mapline != None:
				result.append(mapline)
			mapline = {}

			mapline['name'] = comps[0]
			continue
		tag = comps[0].strip()
		value = comps[1].strip()
		mapline[tag] = value
		#print(tag)

	result.append(mapline)

	return result

def calc_age(birth_date):
	return (date.today() - birth_date) // timedelta(days=365.2425)




# print(comps)

if __name__ != '__main__':
	exit()
birth_date = datetime.date(1975, 1, 15)
datetime_object = datetime.datetime.strptime('1975.8.15', '%Y.%m.%d')

print(birth_date,type(datetime_object))
print(datetime_object,type(datetime_object))
age = calc_age(birth_date)
age = calc_age(datetime_object.date())
print(age)

mapinfo = get_twice_mapinfo()
pattname = r'^(\d{4})년 (\d{1,2})월 (\d{1,2})일.*$'
for rows in mapinfo:
	name = rows['name']
	birthday_str =rows['생년월일']
	formatdate = re.sub(pattname,r'\1.\2.\3',birthday_str)
	datetime_object = datetime.datetime.strptime(formatdate, '%Y.%m.%d')
	age = calc_age(datetime_object.date())
	print(name,formatdate,age)

print(mapinfo)

#print(orgstr)