import neolib.neolib4Win as neolib4Win
import re

str = neolib4Win.GetClipBoard()

print(str)
str = str.replace("\r\n",";\r\n")
neolib4Win.SetClipBoard(str)

print(str)