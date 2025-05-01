import os
path = os.path.dirname(__file__) + "/Convertor"
inputFileName, outputFileName = path + ".in", path + ".out"

d = {str(ord(a)): b for a, b in zip("ăâîșțĂÂÎȘȚ", "aaistAAIST")}

def setChr(c: str) -> str:
    try:
        return d[str(ord(c))]
    except:
        return c

with open(inputFileName, "r", encoding="utf-8") as f, open(outputFileName, "w", encoding="utf-8") as g:
    for line in f:
        g.write("".join([setChr(c) for c in line]))