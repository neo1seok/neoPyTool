import win32clipboard


def GetClipBoard():
	try:
		win32clipboard.OpenClipboard()
		strret = win32clipboard.GetClipboardData( win32clipboard.CF_UNICODETEXT)  # set clipboard data
		win32clipboard.CloseClipboard()

	except TypeError:
		pass

	return strret

def SetClipBoard(str):
	try:
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData( win32clipboard.CF_UNICODETEXT,str)  # set clipboard data
		win32clipboard.CloseClipboard()
	except TypeError:
		pass
