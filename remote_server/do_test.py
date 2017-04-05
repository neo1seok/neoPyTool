from remote_server.remote_client import cleint_test
from  remote_server.remote_client_handler import TestRemoteHandleClientWithOutSocket
import remote_server.test_scenario as test_scenario
def test_input():
	classdebug = TestRemoteHandleClientWithOutSocket(None)

	classdebug.test(test_scenario.list_test_kbd)
	#classdebug.test(test_scenario.list_test_move)
	classdebug.test(test_scenario.list_test_click)
	#classdebug.test(test_scenario.list_test_drag)
	classdebug.test(test_scenario.list_test_str_input)


address = '192.168.0.3'
#address = 'localhost'

cleint_test(address,test_scenario.list_test_kbd)
#cleint_test(address,test_scenario.list_test_move)
# cleint_test(address,test_scenario.list_test_click)
#cleint_test(address,test_scenario.list_test_click_right)

# cleint_test(address,test_scenario.list_test_drag)
#cleint_test(address,test_scenario.list_test_str_input)
vkkey = 'enter'
#cleint_test(address,[ {'cmd': 'kbd_event',	'values' :(vkkey ,'down')},  {'cmd': 'kbd_event', 'values' :(vkkey ,'up')}])

[ {'cmd': 'kbd_event',	'values' :('a' ,'down')}, {'cmd': 'kbd_event', 'values' :('a' ,'up')}]