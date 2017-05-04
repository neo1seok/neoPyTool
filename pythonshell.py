from neotool.neotool_shell_class import *


if __name__ != '__main__':
	exit()

map_class ={
	'set_clip_board_path':SetClipBoardPath,
	'move_best':MoveToBest,
	'move_good':MoveToGood,

}
maparg = neolib.listarg2Map(sys.argv)
if 'cmd' not in maparg:
	cmd = 'set_clip_board_path'
else:
	cmd = maparg['cmd']

map_class[cmd]().Run()



