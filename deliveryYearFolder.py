import os
import re
import shutil
import win32api




print("fuck the mb pgh")

pattern = r"(201[1-9])[a-zA-Z0-9_\-]+\.\w"
pwd = "H:\\DCIM\\Camera\\"
dstpwd = "H:\\DCIM\\"
for path,dirs,files in os.walk(pwd):
    for tmpfile in files :
        fullpath = "\\".join((path, tmpfile))
        match = re.search(pattern, tmpfile)
        if match:

            newdir = dstpwd+match.group(1)+"\\"


            if not os.path.isdir(newdir):
               os.makedirs(newdir)
            if match.group(1) == "2016":
                continue
            
            shutil.move(fullpath,newpath)
        else:
            newdir = dstpwd + "OLD\\"

        newpath = newdir + tmpfile
        print("{0}->{1}".format(fullpath, newpath))
        shutil.move(fullpath, newpath)

