from  remote_server.remote_client_handler import *

from remote_server.remote_client import cleint_test
from  remote_server.remote_client_handler import TestRemoteHandleClientWithOutSocket
import remote_server.test_scenario as test_scenario

server = NeoTCPServer(("localhost", 5510), RemoteHandleClientWithOutRealInput)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()