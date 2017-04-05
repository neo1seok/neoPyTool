from  neolib.neoserver import *
import neolib.neolib as neolib
import win32api
import win32con
import traceback
from remote_server.vk_info import *
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

class RemoteHandleClient(socketserver.BaseRequestHandler):

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

	def setup(self):
		self.init()
		pass
	def	init(self):
		self.map_process ={
			'kbd_event':self.proc_kbd_event,
			'mouse_move': self.proc_mouse_move,
#			'click': self.proc_click,
			'mouse_event':self.proc_mouse_event,
			'input_string': self.proc_input_string

		}
		for idx in range(26):
			ch_cap = bytes([ord('A') + idx])
			ch = bytes([ord(ch_cap) + 0x20])
			self.map_kbd[ch_cap.decode()] = (ch.decode(), True)
			self.map_kbd[ch.decode()] = (ch.decode(), False)
			# print([tmp  for tmp in str(ch)])
			# print([tmp for tmp in ch.decode()])

			#print(type(str(ch)))

		self.snd = neolib.Struct(**{'err':'',	'result':''})

		self.x_res = win32api.GetSystemMetrics(0)
		self.y_res = win32api.GetSystemMetrics(1)

		None

	def proc_input_string(self, values):
		print(self.map_kbd)
		string,dummy = values
		for ch in string:

			print(neolib.Text2HexString(ch))
			vk_code,isshfit = self.map_kbd[ch]
			print(vk_code,isshfit)
			if isshfit : self.proc_kbd_event(('shift','down'))
			self.proc_kbd_event((vk_code,'down'))
			self.proc_kbd_event((vk_code, 'up'))
			if isshfit: self.proc_kbd_event(('shift', 'up'))

	def proc_kbd_event(self,values):
		vk_key,down_up = values
		win32api.keybd_event(VK_CODE[vk_key], 0, win32con.KEYEVENTF_KEYUP  if down_up !='down' else 0, 0)
		#time.sleep(.05)
		None

	def proc_mouse_move(self,values):
		dx, dy = values
		x,y=win32api.GetCursorPos()

		#print(x + dx, y + dy,delay/1000.0)
		win32api.SetCursorPos((x + dx, y + dy))
		#time.sleep(delay/1000.0)
		# dx = values[0]
		# dy = values[1]




		None
	def proc_click(self,values):
		leftright ,dummy = values

		down = win32con.MOUSEEVENTF_LEFTDOWN if leftright == 'left' else win32con.MOUSEEVENTF_RIGHTDOWN
		up = win32con.MOUSEEVENTF_LEFTUP if leftright == 'left' else win32con.MOUSEEVENTF_RIGHTUP

		print(down,up)
		win32api.mouse_event(down, 0, 0, 0, 0)
		win32api.mouse_event(up, 0, 0, 0, 0)

	def proc_mouse_event(self, values):
		leftright,downup = values
		if leftright == 'left':
			event = win32con.MOUSEEVENTF_LEFTDOWN if downup == 'down' else win32con.MOUSEEVENTF_LEFTUP
		else:
			event = win32con.MOUSEEVENTF_RIGHTDOWN if downup == 'down' else win32con.MOUSEEVENTF_RIGHTUP
		win32api.mouse_event(event, 0, 0, 0, 0)

		None
	def recv_from_client(self):
		return self.request.recv(1024).strip()

	def send_to_client(self,buff):
		self.request.sendall(buff.encode())
		#self.clientsocket.send(buff.encode())
	def handle(self):
		self.run()

	def run(self):
		try:


			buff = self.recv_from_client()

			list_rcv_map = json.loads(buff)
			for rcv_map in list_rcv_map:
				if 'delay' not in rcv_map:
					rcv_map['delay'] = 100
				self.rcv = neolib.Struct(**rcv_map)
				print(rcv_map)
				#self.values = neolib.Struct(**self.rcv.values)


				self.map_process[self.rcv.cmd](self.rcv.values)
				time.sleep(self.rcv.delay/1000.0)

			self.snd.result = 'ok'
			self.snd.err = ''

			print(buff)
			if buff == b'':
				raise Exception()

			time.sleep(0.1)

			time.sleep(0.1)
		except Exception as ext:
			formatted_lines = traceback.format_exc().splitlines()
			self.snd.result = 'fail'
			self.snd.err = str(ext) +''.join(formatted_lines)

		finally:
			self.send_to_client(json.dumps(self.snd.get_dict()))




class TestRemoteHandleClientWithOutSocket(RemoteHandleClient):
	'''
		rcv = {'cmd':'kbd',	'values':	[('shift','down'),('a','down'),('a','up'),('shift','up')]}

		rcv = {'cmd':'mouse_down',
		'values':(100,100)
		}

		rcv = {'cmd':'mouse_move',
		'values':(100,100)
					}
		rcv = {'cmd':'mouse_up',
		'values':[(100,100)]
		}

		snd= {
		'value':'',
		'result':'',
		}
		'''

	rcv_buff = b''
	snd_buff = b''



	def recv_from_client(self):
		return self.rcv_buff

	def send_to_client(self, buff):
		self.snd_buff = buff
		print(buff)

	# def test_kbd(self):
	# 	self.rcv_buff = json.dumps()
	# 	self.run()
	#
	# def test_mouse_move(self):
	# 	rcv_map =[]
	#
	# 	for i in range(10):
	# 		rcv_map.append({'cmd': 'mouse_move', 'values': (1, 1)})
	# 	self.rcv_buff = json.dumps(rcv_map)
	# 	self.run()
	#
	# def test_click(self):
	# 	self.rcv_buff = json.dumps(	[{'cmd': 'click', 'values': 'right'}])
	# 	self.run()
	#
	# def test_drag(self):
	#
	# 	rcv_map = []
	# 	rcv_map.append({'cmd': 'mouse_event', 'values': ('down','left')})
	# 	for i in range(10):
	# 		rcv_map.append({'cmd': 'mouse_move', 'values': (10, 10), 'delay': 100})
	#
	# 	rcv_map.append({'cmd': 'mouse_event', 'values': ('release','left')})
	# 	self.rcv_buff = json.dumps(rcv_map)
	# 	self.run()
	# def test_input_string(self):
	# 	self.rcv_buff = json.dumps([{'cmd': 'input_string', 'values': 'RIGHT'}])
	# 	self.run()
	#
	#
	#
	# def click(self,x, y):
	# 	win32api.SetCursorPos((x, y))
	# 	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
	# 	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
	#
	#

	def test(self,list_test_vector):
		self.rcv_buff = json.dumps(list_test_vector)
		self.run()

		None

class RemoteHandleClientWithOutRealInput(RemoteHandleClient):
	def proc_input_string(self, values):
		print('proc_input_string',values)
		None


	def proc_kbd_event(self,values):
		print('proc_kbd_event', values)
		None

	def proc_click(self,values):
		print('proc_click', values)
		None

	def proc_mouse_event(self, values):
		print('proc_mouse_event', values)

		None
	def proc_mouse_move(self,values):
		print('proc_mouse_move', values)
		None
if __name__ == '__main__':
	#HandleServerWithLogging(5510, RemoteHandleClient).run()
	# Create the server, binding to localhost on port 9999
	print('START_SERVER')
	server = NeoTCPServer(( "0.0.0.0", 5510), RemoteHandleClient)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
