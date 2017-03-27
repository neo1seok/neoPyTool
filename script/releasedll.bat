
call setting.bat

echo {0} is level number , {1} is CPU type , {2} is date

del out.txt

neotool.exe -RT TOOLKITRelease -ORG "%TARGETDIR%\REL_LEVEL{0}\{1}\*" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\bin\\" >>out.txt
neotool.exe -RT TOOLKITRelease -ORG "%TARGETDIR%\REL_LEVEL{0}\{1}\%DLLNAME%" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\lib\\" >>out.txt
neotool.exe -RT TOOLKITRelease -ORG "%SRCDLLDIR%\{1}\*.dll" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\bin\\" >>out.txt
neotool.exe -RT TOOLKITRelease -ORG "%SRCDLLDIR%\{1}\*.dll" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\lib\\" >>out.txt
neotool.exe -RT TOOLKITRelease -ORG "%TARGETDIR%\run.level{0}.bat" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\bin\\" >>out.txt
neotool.exe -RT TOOLKITRelease -ORG "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\bin\app.ipst100.server.exe" -DST "%TARGETDIR2%\{2}\REL_LEVEL{0}\SERVER\C#\{1}\bin\app.ipst100.server.level{0}.exe" -MOVE >>out.txt
type out.txt
pause
