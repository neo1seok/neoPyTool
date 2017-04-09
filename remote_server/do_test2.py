from  remote_server.remote_client_handler import *

from remote_server.remote_client import cleint_test
from  remote_server.remote_client_handler import TestRemoteHandleClientWithOutSocket
import remote_server.test_scenario as test_scenario


#HandleServerWithLogging(5510, RemoteHandleClientWithOutRealInput).run()
server = NeoTCPServer( 5510, RemoteHandleClient)
#server = NeoTCPServer( 5510, RemoteHandleClientWithOutRealInput)
ip, port = server.server_address
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)
address = 'localhost'
count = 3
#cleint_test(address,test_scenario.list_test_kbd,count)

#cleint_test(address,test_scenario.list_test_drag,count)
#
#cleint_test(address,test_scenario.list_test_down_move_rdownrup,count)
#cleint_test(address,test_scenario.list_test_move,count)
#cleint_test(address,test_scenario.list_test_click,count)
#cleint_test(address,test_scenario.list_test_click_right,count)
cleint_test(address,test_scenario.list_test_str_input,count)

exit()
cleint_test(ip,test_scenario.mouse_event_list)
cleint_test(ip,test_scenario.list_test_kbd)
cleint_test(ip,test_scenario.list_test_move)
cleint_test(ip,test_scenario.list_test_click)
cleint_test(ip,test_scenario.list_test_click_right)

cleint_test(ip,test_scenario.list_test_drag)
cleint_test(ip,test_scenario.list_test_str_input)

server.shutdown()
server.server_close()