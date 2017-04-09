from remote_server.remote_client import cleint_test
from  remote_server.remote_client_handler import TestRemoteHandleClientWithOutSocket
import remote_server.test_scenario as test_scenario
import time
def test_input():
	classdebug = TestRemoteHandleClientWithOutSocket(None)

	classdebug.test(test_scenario.list_test_kbd)
	#classdebug.test(test_scenario.list_test_move)
	classdebug.test(test_scenario.list_test_click)
	#classdebug.test(test_scenario.list_test_drag)
	classdebug.test(test_scenario.list_test_str_input)


address = '192.168.0.3'
address = 'localhost'

cleint_test(address,test_scenario.mouse_event_list_move)
exit()
cleint_test(address,test_scenario.list_test_kbd)
time.sleep(1)
cleint_test(address,test_scenario.list_test_move)
time.sleep(1)
cleint_test(address,test_scenario.list_test_move_abs)

cleint_test(address,test_scenario.list_test_click)
time.sleep(1)
cleint_test(address,test_scenario.list_test_click_right)
time.sleep(1)

vkkey = 'esc'
cleint_test(address,[ {'cmd': 'kbd_event',	'values' :[(vkkey ,'down'), (vkkey ,'up')]}])
cleint_test(address,test_scenario.list_test_drag)
cleint_test(address,test_scenario.list_test_str_input)
[ {'cmd': 'kbd_event',	'values' :('a' ,'down')}, {'cmd': 'kbd_event', 'values' :('a' ,'up')}]