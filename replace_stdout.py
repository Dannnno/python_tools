import contextlib
import sys


@contextlib.contextmanager
def capture(new_out=sys.stdout, new_err=sys.stderr):
    oldout, olderr = sys.stdout, sys.stderr

    try:
        out = [new_out, new_err]
        sys.stdout, sys.stderr = out
        yield out

    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()