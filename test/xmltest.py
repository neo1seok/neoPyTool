
xml_sro='''
<note>
	<to>Tove</to>
	<from>Jani</from>
	<heading>Reminder</heading>
	<body>Don't forget me this weekend!</body>
</note>
'''
xml_src2='''
<test>
  <song>
	 <title>a</title>
	 <length>4:54</length>
  </song>
  <song>
	 <title>b</title>
	 <length>3:21</length>
  </song>
</test>
'''

from xml.etree.ElementTree import Element, dump

note = Element("note")
to = Element("to")
to.text = "Tove"

note.append(to)
dump(note)
from xml.etree.ElementTree import Element, ElementTree, SubElement, dump, parse, tostring,fromstring



def TestFromFile():
	targetXML = open("test.xml", 'r')

	tree = parse(targetXML)
	root = tree.getroot()

	for element in root.findall("song"):
		print(element.findtext("title"))
		print(element.findtext("length"))

def TestFromString():
	root = fromstring(xml_src2)
	print(root.findall("song"))
	for element in root.findall("song"):
		print(element.findtext("title"))
		print(element.findtext("length"))
def TestFromString2():
	root = fromstring(xml_sro)
	print(root)
	for element in root.findall("note"):
		print(element)
		print(element.findtext("title"))
		print(element.findtext("length"))
if __name__ == '__main__':
	#TestFromFile()
	TestFromString2()