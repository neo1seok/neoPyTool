from  neolib.neoserver import *
import neolib.neolib as neolib
import win32api
import win32con
import traceback
from remote_server.vk_info import *
import socketserver

class EventHandler():
	map_kbd = {
		' ': ('spacebar', False),
		'!': ('1', True),
		'@': ('2', True),
		'{': ('[', True),
		'?': ('/', True),
		':': (';', True),
		'"': ('\'', True),
		'}': (']', True),
		'#': ('3', True),
		'$': ('4', True),
		'%': ('5', True),
		'^': ('6', True),
		'&': ('7', True),
		'*': ('8', True),
		'(': ('9', True),
		')': ('0', True),
		'_': ('-', True),
		'=': ('+', True),
		'~': ('`', True),
		'<': (',', True),
		'>': ('.', True),
	}

	def __init__(self):
		self.x_res = win32api.GetSystemMetrics(0)
		self.y_res = win32api.GetSystemMetrics(1)

		self.map_mouse_event = {
			'ldown': win32con.MOUSEEVENTF_LEFTDOWN,
			'lup': win32con.MOUSEEVENTF_LEFTUP,
			'rdown': win32con.MOUSEEVENTF_RIGHTDOWN,
			'rup': win32con.MOUSEEVENTF_RIGHTUP,
		}
		self.map_kbd_event = {
			'keydown': 0 ,
			'keyup':  win32con.KEYEVENTF_KEYUP ,
		}

		self.map_event_proc = {
			'ldown':self.proc_mouse_downup,
			'lup': self.proc_mouse_downup,
			'rdown': self.proc_mouse_downup,
			'rup': self.proc_mouse_downup,
			'move':self.proc_move,
			'keydown': self.proc_keydownup,
			'keyup': self.proc_keydownup,
			#'input_string':self.proc_input_string

		}
		for idx in range(26):
			ch_cap = bytes([ord('A') + idx])
			ch = bytes([ord(ch_cap) + 0x20])
			self.map_kbd[ch_cap.decode()] = (ch.decode(), True)
			self.map_kbd[ch.decode()] = (ch.decode(), False)
			# print([tmp  for tmp in str(ch)])
			# print([tmp for tmp in ch.decode()])

			#print(type(str(ch)))
		None

	def set_cursor_pos(self, x, y):
		win32api.SetCursorPos((x, y))

	def mouse_event(self, event):
		win32api.mouse_event(event, 0, 0, 0, 0)
	def kbd_event(self,vk_key,down_up):
		event = self.map_kbd_event[down_up]
		win32api.keybd_event(VK_CODE[vk_key], 0, event, 0)

	def input_string(self, string):
		for ch in string:
			print(neolib.Text2HexString(ch))
			vk_code,isshfit = self.map_kbd[ch]
			print(vk_code,isshfit)
			if isshfit : self.kbd_event('shift','keydown')
			self.kbd_event(vk_code,'keydown')
			self.kbd_event(vk_code, 'keyup')
			if isshfit: self.kbd_event('shift', 'keyup')

	def proc_mouse_downup(self,eventname,param):
		x, y = param
		#x,y = self.get_point(pointvalue)
		print(x,y)
		if x != -1 and  y != -1:
			x, y = self.get_point(x, y)
			self.set_cursor_pos(x,y)

		event =self.map_mouse_event[eventname]
		self.mouse_event(event)

	def proc_move(self,eventname,param):
		x, y = param
		x, y = self.get_point(x,y)
		#x,y = self.get_point(pointvalue)
		print(x,y)
		self.set_cursor_pos(x,y)
	def proc_keydownup(self,eventname,param):
		self.kbd_event(param[0],eventname)

		None

	def run(self,eventname,param,delay):
		event_proc = self.map_event_proc[eventname]
		print('event proc name',event_proc.__name__)
		event_proc(eventname,param)
		#
		# x,y = param
		#
		# #x,y = self.get_point(pointvalue)
		# print(x,y)
		# self.set_cursor_pos(x,y)
		# # win32api.SetCursorPos((x, y))
		#
		# if eventname in self.map_event:
		# 	event =self.map_event[eventname]
		# 	self.mouse_event(event)
		time.sleep(delay / 1000.0)
		# if leftright == 'left':
		# 	event = win32con.MOUSEEVENTF_LEFTDOWN if downup == 'ldown' else win32con.MOUSEEVENTF_LEFTUP
		# else:
		# 	event = win32con.MOUSEEVENTF_RIGHTDOWN if downup == 'ldown' else win32con.MOUSEEVENTF_RIGHTUP

		None

	def get_point(self,x,y):

		ratex = x / self.width
		ratey = y /self.height
		curx = int(self.x_res * ratex)
		cury = int(self.y_res * ratey)
		return curx,cury

	def set_size(self,value):
		self.width,self.height = value

class EventHandlerWithOutRealInput(EventHandler):
	def set_cursor_pos(self, x, y):
		# win32api.SetCursorPos((x, y))
		print(x,y)

	def mouse_event(self, event):
		#win32api.mouse_event(event, 0, 0, 0, 0)
		print(event)

	def kbd_event(self, vk_key, down_up):
		None