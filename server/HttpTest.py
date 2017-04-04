import http.server
import socketserver

class TestHttpRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header(b"Content-type", b"text/html")
		self.end_headers()

	def do_GET(self):
		self.send_response(200)
		self.send_header(b"Content-type", b"text/html")
		self.end_headers()
		print(self.wfile)
		self.wfile.write(b"<html><head><title>Title goes here.</title></head>")
		self.wfile.write(b"<body><p>This is a test.</p>")
		# If someone went to "http://something.somewhere.net/foo/bar/",
		# then s.path equals "/foo/bar/".
		input = "<p>You accessed path: %s</p>" % self.path
		self.wfile.write(input.encode())
		self.wfile.write(b"</body></html>")
		#self.wfile.close()
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), TestHttpRequestHandler)

print("serving at port", PORT)
httpd.serve_forever()