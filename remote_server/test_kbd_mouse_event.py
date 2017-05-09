import win32clipboard
import win32process
import win32api
import win32con
import neolib.neoutil as neolib
import time

# Giant dictonary to hold key name and VK value



class KeybdEventHandler:

	def __init__(self):

		None


	def press(self,*args):
		'''
		one press, one release.
		accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
		'''
		for i in args:
			win32api.keybd_event(self.VK_CODE[i], 0, 0, 0)
			time.sleep(.05)
			win32api.keybd_event(self.VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)

	def press(self,*args):
		'''
		one press, one release.
		accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
		'''
		for i in args:
			win32api.keybd_event(self.VK_CODE[i], 0, 0, 0)
			time.sleep(.05)
			win32api.keybd_event(self.VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)


	def pressAndHold(self,*args):
		'''
		press and hold. Do NOT release.
		accepts as many arguments as you want.
		e.g. pressAndHold('left_arrow', 'a','b').
		'''
		for i in args:
			win32api.keybd_event(self.VK_CODE[i], 0, 0, 0)
			time.sleep(.05)


	def pressHoldRelease(self,*args):
		'''
		press and hold passed in strings. Once held, release
		accepts as many arguments as you want.
		e.g. pressAndHold('left_arrow', 'a','b').

		this is useful for issuing shortcut command or shift commands.
		e.g. pressHoldRelease('ctrl', 'alt', 'del'), pressHoldRelease('shift','a')
		'''
		for i in args:
			win32api.keybd_event(self.VK_CODE[i], 0, 0, 0)
			time.sleep(.05)

		for i in args:
			win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)
			time.sleep(.1)



	def release(self,*args):
		'''
		release depressed keys
		accepts as many arguments as you want.
		e.g. release('left_arrow', 'a','b').
		'''
		for i in args:
			win32api.keybd_event(self.VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)

	def process_unit(self,vk_name):
		win32api.keybd_event(self.VK_CODE[vk_name], 0, 0, 0)

	def release_unit(self, vk_name):
		win32api.keybd_event(self.VK_CODE[vk_name], 0, win32con.KEYEVENTF_KEYUP, 0)
	def process_release_unit(self,vk_name):
		self.process_unit(vk_name)
		time.sleep(.05)
		self.release_unit(vk_name)


	def typer(self,string=None, *args):
		##    time.sleep(4)
		map_kbd =\
		{
			' ':('spacebar',False),
			'!':('1',True),
			'@':('2',True),
			'{':('[',True),
			'?':('/',True),
			':':(';',True),
			'"':('\'',True),
			'}':(']',True),
			'#':('3',True),
			'$':('4',True),
			'%':('5',True),
			'^':('6',True),
			'&':('7',True),
			'*':('8',True),
			'(':('9',True),
			')':('0',True),
			'_':('-',True),
			'=':('+',True),
			'~':('`',True),
			'<':(',',True),
			'>':('.',True),
		}
		for idx  in range(26):
			ch_cap = bytes([ord('A')+idx])
			ch = bytes([ord(ch_cap) + 0x20])
			map_kbd[ch_cap] = (''+str(ch),True)
			print(ch)
		print(map_kbd)

		# for i in string:
		# 	if i == ' ':
		# 		win32api.keybd_event(VK_CODE['spacebar'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['spacebar'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '!':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['1'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['1'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '@':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['2'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['2'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '{':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['['], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['['], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '?':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['/'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['/'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == ':':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE[';'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE[';'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '"':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['\''], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['\''], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '}':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE[']'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE[']'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '#':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['3'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['3'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '$':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['4'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['4'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '%':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['5'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['5'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '^':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['6'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['6'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '&':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['7'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['7'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '*':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['8'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['8'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '(':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['9'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['9'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == ')':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['0'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['0'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '_':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['-'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['-'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		#
		# 	elif i == '=':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['+'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['+'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '~':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['`'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['`'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '<':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE[','], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE[','], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == '>':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['.'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['.'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'A':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['a'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['a'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'B':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['b'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['b'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'C':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['c'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['c'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'D':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['d'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['d'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'E':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['e'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['e'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'F':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['f'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['f'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'G':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['g'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['g'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'H':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['h'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['h'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'I':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['i'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['i'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'J':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['j'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['j'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'K':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['k'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['k'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'L':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['l'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['l'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'M':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['m'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['m'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'N':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['n'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['n'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'O':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['o'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['o'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'P':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['p'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['p'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'Q':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['q'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['q'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'R':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['r'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['r'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'S':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['s'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['s'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'T':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['t'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['t'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'U':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['u'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['u'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'V':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['v'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['v'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'W':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['w'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['w'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'X':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['x'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['x'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'Y':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['y'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['y'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		# 	elif i == 'Z':
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, 0, 0)
		# 		win32api.keybd_event(VK_CODE['z'], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE['left_shift'], 0, win32con.KEYEVENTF_KEYUP, 0)
		# 		win32api.keybd_event(VK_CODE['z'], 0, win32con.KEYEVENTF_KEYUP, 0)
		#
		#
		# 	else:
		# 		win32api.keybd_event(VK_CODE[i], 0, 0, 0)
		# 		time.sleep(.05)
		# 		win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)


KeybdEventHandler().typer('')






