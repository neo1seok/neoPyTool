
from tornado.ioloop import IOLoop,
from  tornado.tcpserver import TCPServer,bind_sockets


sockets = bind_sockets(8888)
tornado.process.fork_processes(0)
server = TCPServer()
server.add_sockets(sockets)
IOLoop.current().start()