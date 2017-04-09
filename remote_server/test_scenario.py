import simplejson as json
list_test_kbd = [ 				 {'cmd' :'kbd_event',	'values':	[('ctrl' ,'down'), ('a' ,'down'), ('a' ,'up'),	 ('ctrl' ,'up')]}]

list_test_drag = [ 				{'cmd': 'mouse_event', 'values': [('left','down' )]},
								  {'cmd': 'mouse_move', 'values':[(10, 10),(10, 10),(10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10)]},
								  {'cmd': 'mouse_event', 'values': [( 'left','up')]}]

list_test_move = [ 				  {'cmd': 'mouse_move', 'values':[(10, 10),(10, 10),(10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10), (10, 10)]}, ]

list_test_move_abs = [ 				  {'cmd': 'set_size', 'values': [(100,100)]},
										{'cmd': 'mouse_move_abs', 'values': [(10, 10),(12, 10),(14, 10), (16, 10)]},

									 ]

mouse_event_list = [ 				  {'cmd': 'set_size', 'values': [(100,100)]},
										{'cmd': 'mouse_event_list', 'values': [
											('down',10|(10<<16)),
											('up',10|(10<<16)),
											('move',10|(10<<16)),
											('move',12|(10<<16)),
											('move',14|(10<<16)),
											('move',15|(10<<16)),
											('move',16|(10<<16)),
											('rdown',50|(50<<16)),
											('rup',50|(50<<16)),


										]},

									 ]
mouse_event_list_move = [ 				  {'cmd': 'set_size', 'values': [(100,100)]},
										{'cmd': 'mouse_event_list', 'values': [

											('move',10|(10<<16)),
											('move',12|(10<<16)),
											('move',14|(10<<16)),
											('move',15|(10<<16)),
											('move',16|(10<<16)),


										]},

									 ]

list_test_click =				[ 				{'cmd': 'mouse_event', 'values': [('left','down' ), ( 'left','up')]}]

list_test_click_right =				[ {'cmd': 'mouse_event', 'values': [('right','down' ), ( 'right','up')]}]


list_test_str_input = [{'cmd': 'input_string', 'values': [('abcdefghijklmnopqrstuvz','')]}]

if __name__ == '__main__':
	print(json.dumps(list_test_kbd))