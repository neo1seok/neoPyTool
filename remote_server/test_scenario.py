import simplejson as json
list_test_kbd = [ 				 {'cmd' :'kbd_event',	'values':	('ctrl' ,'down')},
								  {'cmd': 'kbd_event',	'values' :('a' ,'down')},
								  {'cmd': 'kbd_event', 'values' :('a' ,'up')},
								  {'cmd': 'kbd_event', 'values' :('ctrl' ,'up')}]

list_test_drag = [ 				{'cmd': 'mouse_event', 'values': ('left','down' )},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_move', 'values': (10, 10)},
								  {'cmd': 'mouse_event', 'values': ( 'left','up')}]

list_test_move = [ 				  {'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)},
									{'cmd': 'mouse_move', 'values': (10, 10)}		 ]

list_test_click =				[ 				{'cmd': 'mouse_event', 'values': ('left','down' )},
								  {'cmd': 'mouse_event', 'values': ( 'left','up')}]

list_test_click_right =				[ {'cmd': 'mouse_event', 'values': ('right','down' )},
								  {'cmd': 'mouse_event', 'values': ( 'right','up')}]


list_test_str_input = [{'cmd': 'input_string', 'values': ('abcdefghijklmnopqrstuvz','')}]

if __name__ == '__main__':
	print(json.dumps(list_test_kbd))