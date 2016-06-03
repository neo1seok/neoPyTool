import os
import re
import shutil
import win32api
import win32gui
import win32con
import time
import datetime
import sys
import glob

import win32clipboard
import neolib
import base64


class TestDisplay(neolib.NeoTestClasss):
    def doRun(self):
        nums = []

        def fib(pyHwnd, n):
            str = win32gui.GetClassName(pyHwnd)
            if str == "PuTTY":
                nums.append(pyHwnd)

            print(str)

        print(__name__)

        yesterday = datetime.datetime(2016, 5, 12, 6, 45)
        ans_time = int(time.mktime(yesterday.timetuple()))
        print(ans_time)

        list = win32api.EnumDisplayMonitors(None, None);
        PyHANDLE = win32gui.FindWindow("PuTTY", None);
        print(list)
        print(PyHANDLE)

        win32gui.EnumWindows(lambda n, m: print(n), 0)

        print(nums)



class TestTmp(neolib.NeoTestClasss):
    def doRun(self):
        None

class ChanageMp3Title(neolib.NeoTestClasss):
    maptitle = {'데려다줄래': '01', 'L.I.E': '02', '알면서': '03', 'HELLO(하니SOLO)': '04', 'CREAM': '05', '3%(솔지SOLO)': '06',
                'ONLYONE': '07', '당연해': '08', '냠냠쩝쩝(정화&혜린)': '09', '여름,가을,겨울,봄': '10', 'GOOD': '11',
                'HOTPINK(REMIX)': '12',
                'L.I.E(JANNABIMIX)': '13',}
    basepath = 'E:\\mp3\\EXID STREET'

    def doRun(self):


        for file in glob.glob(basepath + '\\*.mp3'):
            fname = os.path.basename(file)

            realname = re.sub(r"(.+)_EXID\(이엑스아이디\)_STREET\.mp3", r"\1", fname)

            strcmp = realname.replace(" ", "")
            strcmp = strcmp.upper()
            # print(strcmp in maptitle.keys())
            newfilename = "{0}\\{1}.{2}.mp3".format(basepath, self.maptitle[strcmp], realname)
            print(newfilename)
            shutil.move(file, newfilename)
            aaa = 34

class TestHexString(neolib.NeoTestClasss):
    def doRun(self):
        # result = bytearray.fromhex('deadbeef')
        byteform = neolib.HexString2Text(
            '02 30 34 31 37 30 39 32 30 36 30 49 30 4B 4B 1C 32 33 34 35 36 37 38 39 30 31 1C 30 33 36 37 1C 36 31 35 33 31 30 39 34 31 32 38 30 1C 30 30 31 1C 45 4E 30 37 23 23 23 53 4D 54 2D 44 33 35 30 43 31 31 30 31 23 23 23 23 53 4D 54 2D 54 32 32 34 31 30 30 31 30 30 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 30 31 34 30 41 6C 42 77 63 48 42 77 63 44 41 77 4D 44 41 78 55 45 32 46 46 46 41 41 41 41 49 41 41 41 42 41 71 6F 2B 50 31 4D 73 4C 5A 42 75 36 49 67 6D 78 35 6A 4A 32 44 36 5A 46 6D 64 76 46 35 63 62 58 7A 57 65 56 53 56 61 42 4D 35 68 32 32 65 6C 42 51 71 4A 68 47 69 54 4E 59 6E 51 68 79 2B 4F 38 33 50 4C 67 78 6F 64 35 51 4C 66 7A 52 4E 72 2F 30 64 6B 46 50 52 44 79 39 6B 69 6E 41 34 58 56 34 58 41 47 63 79 6D 56 67 2F 48 61 1C 1C 31 30 30 30 1C 1C 39 30 1C 31 36 30 36 30 31 1C 31 1C 30 31 1C 30 35 31 30 30 30 31 30 1C 31 30 32 30 33 30 34 30 35 30 36 30 37 30 38 30 38 30 31 34 30 36 30 36 30 31 30 33 41 30 41 38 30 32 41 41 42 42 43 43 44 44 30 32 38 32 30 30 30 30 30 30 38 38 30 30 31 36 30 36 30 31 30 30 37 43 30 30 31 45 30 33 30 30 20 20 36 30 32 38 43 30 32 32 41 30 31 31 30 30 30 31 30 30 30 30 31 36 41 30 30 30 30 30 30 30 32 35 30 31 30 34 30 32 30 30 30 31 30 33 36 36 30 35 31 30 1C 1C 1C 03 39 42 34 38',
            'utf-8')
        print(byteform)
        resttr = bytes.fromhex(
            '416C427763484277634441774D44417855453246464641414141494141414241716F2B50314D734C5A42753649676D78356A4A3244365A466D647646356362587A576556535661424D35683232656C4251714A684769544E596E5168792B4F3833504C67786F6435514C667A524E722F30646B4650524479396B696E413458563458414763796D56672F4861').decode(
            'utf-8')
        print(resttr)
        result = base64.standard_b64decode(resttr)
        hexstring = ''.join('{:02X} '.format(x) for x in result)
        print(result)
        print(hexstring)

class TestDrowDC(neolib.NeoTestClasss):
    def doRun(self):
        hdc = win32gui.GetDC(None, )
        cpen = win32gui.CreatePen(win32con.PS_COSMETIC, 10, win32api.RGB(255, 0, 0))
        coldpen = win32gui.SelectObject(hdc, cpen)

        win32gui.Rectangle(hdc, 100, 100, 300, 300)

        coldpen = win32gui.SelectObject(hdc, coldpen)
        win32gui.ReleaseDC(None, hdc)



class TestChangePath(neolib.NeoTestClasss):
    def doRun(self):
        path = "Z:\\Smartro\\산출물\\"

        print(path)
        fp = open(path + "out.txt", "w")
        for path, dirs, files in os.walk(path):
            for tmpfile in files:
                fullpath = "\\".join((path, tmpfile))
                print(tmpfile)
                fname, ext = os.path.splitext(fullpath)
                fp.write(tmpfile + "\t" + re.sub(r"\.", r"", ext) + "\n")
            break

        print(re.sub("a", "", "testaa"))
        print(neolib.listarg2Map(list))

        fp.close()


TestDisplay().doRun()


print(neolib.Text2HexString("pPpp", 'utf-8', ' '))

exit()

exit()


exit();


exit()


exit()

basepath = 'D:\\PROJECT\\스마트로\\TEMP\\SMARTRO_new3\\SMARTRO\\bin'

fp = open("D:\\PROJECT\\스마트로\\TEMP\\SMARTRO_new3\\SMARTRO\\bin\\out.txt", "w")
for file in glob.glob(basepath + '\\*.*'):
	fp.write(os.path.basename(file) + "\n")

files = list(map(lambda x: os.path.basename(x), glob.glob(basepath + '\\*.*')))
mapfiles = dict((os.path.basename(v), v) for v in glob.glob(basepath + '\\*.*'))

print("FILES:")
print(mapfiles)

fp.close()

print(sys.argv)

exit()
