import simplejson as json
list_test_kbd = [ 				 {'cmd' :'input_event',	'values':	[('keydown','ctrl' ,), ('keydown','a' ), ('keyup','a' ),	 ('keyup','ctrl')]}]
list_test_drag = [ 				 {'cmd': 'set_size', 'values': [(100,100)]},
								   {'cmd': 'input_event', 'values': [('ldown',50,50 ),	('move', 50, 50),('move', 52, 52),('move', 54, 54),
																	('move', 55, 55),('move', 56, 56),( 'lup',-1,-1)]}]


list_test_down_move_rdownrup = [ 				  {'cmd': 'set_size', 'values': [(100,100)]},
										{'cmd': 'input_event', 'values': [
											('ldown', 10, 10),
											('lup', 10, 10),
											('move', 10, 10),
											('move', 12, 10),
											('move', 14, 10),
											('move', 15, 10),
											('move', 16, 10),
											('rdown', 50, 50),
											('rup', 50, 50),


										]},

									 ]
list_test_move = [ 				  {'cmd': 'set_size', 'values': [(100,100)]},
										{'cmd': 'input_event', 'values': [

											('move', 10, 10),
											('move', 12, 10),
											('move', 14, 10),
											('move', 15, 10),
											('move', 16, 10),


										]},

									 ]

list_test_click =				[ 				{'cmd': 'input_event', 'values': [('ldown',-1,-1 ), ( 'lup',-1,-1)]}]

list_test_click_right =				[ {'cmd': 'input_event', 'values': [('rdown',-1,-1 ), ( 'rup',-1,-1)]}]


list_test_str_input = [{'cmd': 'input_string', 'values': [('abcdefghijklmnopqrstuvz','')]}]

if __name__ == '__main__':
	print(json.dumps(list_test_kbd))