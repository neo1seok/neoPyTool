import http.server
import socketserver
import re
import os
from logging import handlers
from urllib.parse import urlparse
import neolib.neoutil as neolib
import traceback
from neolib.neoserver import *
from neotool.neotool_class import *
import  json
str_out = ''


def http_pytool(cmd,param=''):
	global str_out
	str_out = ""

	def print_view(*args):
		global str_out
		str_out += ",".join(args)
		None

	print("http_pytool",param.split('&'))
	try:
		maparg = dict([  query.split('=') for query in param.split('&')])
	except:
		maparg = {}

	main_process(cmd, maparg,print_view=print_view)
	return {'print_view':str_out}

class HttpRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(self):
		logger.debug("do_HEAD")
		self.send_response(200)
		self.send_header(b"Content-type", b"text/html")
		self.end_headers()

	def log_message(self, format, *args):
		logger.debug("log_message:"+format,*args)
		None
	def do_GET(self):
		logger.debug("do_GET")


		try:
			self.send_response(200)
			self.send_header(b"Content-type", b":application/json; charset=utf-8")


			self.end_headers()



			o = urlparse(self.path)
			str_path = o.path

			if str_path == '/':
				str_path = '/index.html'
			logger.debug("o:{0}".format(o))
			logger.debug("PATH:{0}".format(PATH))
			filename, file_extension = os.path.splitext(str_path)

			print("test",filename, file_extension)
			if file_extension.lower() == '.do':
				cmd = filename[1:]
				json_res = http_pytool(cmd,o.query)

				contents = json.dumps(json_res)
				#neolib.json_pretty(json_res)
				contents = neolib.StrFromFile('rsc' + "/index.html");
				logger.debug("contents:{0}".format(contents))

				self.wfile.write(contents.encode())
				return
			# self.send_header(b"Content-type", b"text/html")
			# self.end_headers()
			contents = neolib.StrFromFile('rsc' + str_path);
			self.wfile.write(contents.encode())
		except Exception as ext :
			formatted_lines = traceback.format_exc().splitlines()

			logger.debug("exeption")
			logger.debug("{0}\n{1}".format('\n'.join(formatted_lines),ext))



PORT = 8000
maparg = neolib.listarg2Map(sys.argv)
PATH = 'rsc'

handler = handlers.TimedRotatingFileHandler(filename="C:/LOG/http_log.log", when='D')
logger = neolib.create_logger("tool", handler=handler)


try:
	PORT = int(maparg["port"])
	PATH = maparg["path"]
except:
	None
logger.debug("START:{0} {1}".format(PORT,PATH))


#httpd = socketserver.TCPServer(('0.0.0.0', PORT), http.server.SimpleHTTPRequestHandler)
httpd = NeoTCPServer( PORT, HttpRequestHandler)
#httpd = socketserver.TCPServer(('0.0.0.0', PORT), HttpRequestHandler)
logger.debug("serving at port:{0}".format(PORT))
httpd.serve_forever()