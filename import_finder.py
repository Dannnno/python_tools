import re
import os
from functools import partial
from itertools import imap as imp


matchers = map(re.compile, [r"from[ ][^ ]*[ ]import[ ][^ ]*",
                                r"from[ ][^ ]*[ ]import[ ][^ ]*[ ]as[ ]*",
                                r"import[ ][^ ]*",
                                r"import[ ][^ ]*[ ]as[ ]*",
                                r"[^ ]*[ ]=[ ]__import__\('[^']*'\)",
                                r"importlib.import_module\([^)]*\)"])
                                
                                
def find_imports(afile):
    import time as t
    for line in afile:
        line = line.rstrip().lstrip()
        for prog in matchers:
            if prog.match(line):
                print line, matchers.index(prog)
                break
                

if __name__ == '__main__':
    with open("C:\\Users\\Dan\\Desktop\\Programming\\GitHub\\python_tools\\import_finder.py", "r") as f:
        f.seek(0)
        find_imports(f)
