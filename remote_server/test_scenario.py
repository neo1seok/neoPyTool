
list_test_kbd = [ 				 {'cmd' :'kbd_event',	'params':	('ctrl' ,'down')},
								  {'cmd': 'kbd_event',	'params' :('a' ,'down')},
								  {'cmd': 'kbd_event', 'params' :('a' ,'up')},
								  {'cmd': 'kbd_event', 'params' :('ctrl' ,'up')}]

list_test_drag = [ 				{'cmd': 'press_release', 'params': ('press' ,'left')},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'mouse_move', 'params': (10, 10)},
								  {'cmd': 'press_release', 'params': ('release', 'left')}]

list_test_move = [ 				  {'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)},
									{'cmd': 'mouse_move', 'params': (10, 10)}		 ]

list_test_click =				[{'cmd': 'click', 'params': ('left' ,'')}]
list_test_click_right =				[{'cmd': 'click', 'params': ('right' ,'')}]
list_test_str_input = [{'cmd': 'input_string', 'params': ('abcdefghijklmnopqrstuvz','')}]