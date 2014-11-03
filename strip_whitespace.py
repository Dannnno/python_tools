try:
    import cStringIO as IO
except ImportError:
    import StringIO as IO
finally:
    import sys


afile = sys.argv[1]

io = IO.StringIO()

with open(afile, "r") as rf:
    for line in rf:
        temp = line.rstrip()
        temp.replace("\t", "    ")
        io.write(temp + "\n")

with open(afile, "w") as wf:
    wf.write(io.get_value())
