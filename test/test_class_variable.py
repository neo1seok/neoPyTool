class Struct:
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def get_dict(self):
		return dict(self.__dict__)

	def from_dict(self,dict):
		self.__dict__.update(dict)
class Dog:

	kind = 'canine'         # class variable shared by all instances

	def __init__(self, name):
		self.name = name    # instance variable unique to each instance

class Dog2:

	tricks = []             # mistaken use of a class variable
	id = 3
	def __init__(self, name):
		self.name = name

	def add_trick(self, trick):
		self.tricks.append(trick)
d = Dog('Fido')
e = Dog('Buddy')
print(d.kind)
print(e.kind)
print(d.name)
print(e.name)

d = Dog2('Fido')
e = Dog2('Buddy')
Dog2.id =1818

d.add_trick('roll over')
e.add_trick('play dead')

Dog2.tricks.append('1818')


print(d.tricks)
print(Dog2.tricks)

print(d.id)
print(Dog2.id)

exit()
class AAAAAA:
	id = 1
	list_process = []
	list_process1 = []
	struct = Struct(**{'a': 2})
	name = "김철수"
	def __init__(self):


		self.list_process.extend([2323,2323,2323,23])
		self.list_process1.append(3222)
		#self.id += 1
		self.name += "김철수"

	def set_id(self):
		self.id = 2222
	def view(self):
		print(len(self.list_process),self.list_process,self.id)
		print(len(self.list_process1), self.list_process1, self.id)
		print(self.name)
		print(self.struct.get_dict())

print(dir(AAAAAA))
a = AAAAAA()
b = AAAAAA()
a.id =3
print(a.id)

print(b.id)

for idx in range(2):
	# AuthProcessWithWebServer().check_listcoutn()
	aaaaa = AAAAAA()
	aaaaa.struct.a += 1
	aaaaa.view()
