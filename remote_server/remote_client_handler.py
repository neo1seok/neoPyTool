from remote_server.event_haldler import *
import socketserver

class RemoteHandleClient(socketserver.BaseRequestHandler):



	def setup(self):
		self.init()
		pass
	def	init(self):
		self.map_process ={
# 			'kbd_event':self.proc_kbd_event,
# 			'mouse_move': self.proc_mouse_move,
# #			'click': self.proc_click,
# 			'mouse_event':self.proc_mouse_event,
			'input_event': self.proc_input_event,

			'input_string': self.proc_input_string,
#			"mouse_move_abs":self.proc_mouse_move_abs,
			"set_size": self.proc_set_size

		}


		self.snd = neolib.Struct(**{'err':'',	'result':''})


		self.event_handler = EventHandler()
		None


	def proc_input_string(self, values):
		#print(self.map_kbd)
		for value in values:
			string,dummy = value
			self.event_handler.input_string(string)
			# for ch in string:
			#
			# 	print(neolib.Text2HexString(ch))
			# 	vk_code,isshfit = self.event_handler.map_kbd[ch]
			# 	print(vk_code,isshfit)
			# 	if isshfit : self.proc_kbd_event(('shift','down'))
			# 	self.proc_kbd_event((vk_code,'down'))
			# 	self.proc_kbd_event((vk_code, 'up'))
			# 	if isshfit: self.proc_kbd_event(('shift', 'up'))

	def proc_kbd_event(self,values):
		for value in values:
			vk_key,down_up = value
			win32api.keybd_event(VK_CODE[vk_key], 0, win32con.KEYEVENTF_KEYUP  if down_up !='down' else 0, 0)
		#time.sleep(.05)
		None

	def proc_set_size(self, values):

		self.event_handler.set_size(values[0])


	def proc_mouse_move_abs(self,values):
		for value in values:
			for tmp in value:
				dx, dy,width,height = tmp
			#curx,cury=win32api.GetCursorPos()
			ratex = dx/width
			ratey = dy/height
			curx = int(self.x_res*ratex)
			cury = int(self.y_res*ratey)

			#print(x + dx, y + dy,delay/1000.0)
			win32api.SetCursorPos((curx, cury))
			#time.sleep(delay/1000.0)
			# dx = values[0]
			# dy = values[1]

	def proc_mouse_move(self,values):
		for value in values:
			dx, dy = value
			curx,cury=win32api.GetCursorPos()


			#print(x + dx, y + dy,delay/1000.0)
			win32api.SetCursorPos((curx + dx, curx + dy))
			#time.sleep(delay/1000.0)
			# dx = values[0]
			# dy = values[1]




		None
	def proc_click(self,values):
		for value in values:
			leftright ,dummy = value

			down = win32con.MOUSEEVENTF_LEFTDOWN if leftright == 'left' else win32con.MOUSEEVENTF_RIGHTDOWN
			up = win32con.MOUSEEVENTF_LEFTUP if leftright == 'left' else win32con.MOUSEEVENTF_RIGHTUP

			print(down,up)
			win32api.mouse_event(down, 0, 0, 0, 0)
			win32api.mouse_event(up, 0, 0, 0, 0)

	def proc_mouse_event(self, values):
		for value in values:
			leftright,downup = value
			if leftright == 'left':
				event = win32con.MOUSEEVENTF_LEFTDOWN if downup == 'down' else win32con.MOUSEEVENTF_LEFTUP
			else:
				event = win32con.MOUSEEVENTF_RIGHTDOWN if downup == 'down' else win32con.MOUSEEVENTF_RIGHTUP
			win32api.mouse_event(event, 0, 0, 0, 0)

		None


		# print(x + dx, y + dy,delay/1000.0)




	def proc_input_event(self, values):
		for value in values:
			eventname= value[0]
			self.event_handler.run(eventname, value[1:],self.rcv.delay)




	def recv_from_client(self):
		buff = b''
		while True:
			unitbuff = self.request.recv(1024)
			buff+=unitbuff
			if len(unitbuff) != 1024: break
		return buff.strip()

	def send_to_client(self,buff):
		self.request.sendall(buff.encode())
		#self.clientsocket.send(buff.encode())
	def handle(self):
		print('start handle')
		while True:
			try:
				self.run()
			except:
				break
		print('end handle')
	def run(self):
		try:

			print('receiving')
			buff = self.recv_from_client()

			print(buff)
			if buff == b'':
				raise Exception()
			print('received')

			list_rcv_map = json.loads(buff)
			for rcv_map in list_rcv_map:
				if 'delay' not in rcv_map:
					rcv_map['delay'] = 100
				self.rcv = neolib.Struct(**rcv_map)
				#print(rcv_map)
				#self.values = neolib.Struct(**self.rcv.values)

				proc = self.map_process[self.rcv.cmd]
				print("process:",proc.__name__)
				proc(self.rcv.values)
				time.sleep(self.rcv.delay/1000.0)

			self.snd.result = 'ok'
			self.snd.err = ''




		except Exception as ext:
			print('Exception',ext)
			formatted_lines = traceback.format_exc().splitlines()
			print('Exception', ext,formatted_lines)
			self.snd.result = 'fail'
			self.snd.err = str(ext) +''.join(formatted_lines)
			raise ext

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

	def init(self):
		RemoteHandleClient.init(self)
		self.event_handler = EventHandlerWithOutRealInput()
		None

	def print_values(self,):
		None

	def proc_input_string(self, values):

		None


	def proc_kbd_event(self,values):

		None

	def proc_click(self,values):

		None

	def proc_mouse_event(self, values):


		None
	def proc_mouse_move(self,values):

		None

	def proc_mouse_move_abs(self,values):

		None
	# def proc_mouse_event_list(self,values):
	# 	None
if __name__ == '__main__':
	#HandleServerWithLogging(5510, RemoteHandleClient).run()
	# Create the server, binding to localhost on port 9999
	print('START_SERVER')
	server = NeoTCPServer( 5510, RemoteHandleClient)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
