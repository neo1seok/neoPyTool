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




cleint_test(test_scenario.list_test_kbd)
cleint_test(test_scenario.list_test_move)
cleint_test(test_scenario.list_test_click)
cleint_test(test_scenario.list_test_drag)
cleint_test(test_scenario.list_test_str_input)

