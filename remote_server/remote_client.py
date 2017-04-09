import socket
import remote_server.test_scenario as test_scenario
import simplejson as json
def cleint_test(address,list_test,count =1):
	# create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# get local machine name
	#host = socket.gethostname()
	#host = 'localhost'
	#host = "192.168.0.3"

	port = 5510
	#port = 51717

	# connection to hostname on the port.
	s.connect((address, port))



	for idx in range(count):
		s.send(json.dumps(list_test).encode())
		tm = s.recv(1024)

		# s.send(json.dumps(list_test).encode())
		# tm = s.recv(1024)
		# print(tm)

		# s.send(json.dumps(list_test).encode())
		# tm = s.recv(1024)
		print(tm)

	s.close()

	print("The time got from the server is %s" % tm.decode('ascii'))


