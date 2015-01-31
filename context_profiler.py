"""This module provides a simple wrapper for the builtin Profile object,
allowing it to be used as a context manager.  Thus, instead of having to call

>>> import profile
>>> profile.run("some_function()")

repeatedly, one is able to instead use a context manager and then place all
relevant function calls and statements within the indented blocks, like so.

>>> with ContextProfiler() as cp:
...     some_function()
"""

try:
    import cProfile as Profile
except ImportError:
    import profile as Profile
finally:
    import pstats
    import sys


class ContextProfiler(Profile.Profile):
    """A python profiler that can function as a context manager.

    Parameters
    ----------
    sortby : string, optional
        How you would like the results to be sorted. Default is 'cumulative'
    stream : file-like
        The stream or file to which the result should be output

    Attributes
    ----------
    stream
    """

    _stream = None

    def __init__(self, sortby='cumulative', stream=sys.stdout, **kwargs):
        super(ContextProfiler, self).__init__(**kwargs)
        self.sortby = sortby
        self.stream = stream

    @property
    def stream(self):
        """The stream that the results of the code profiling will be written to.
        """

        return self._stream

    @stream.setter
    def stream(self, new_stream):
        try:
            new_stream.write(unicode(''))
        except (AttributeError,   # Isn't a file-like object
                IOError,   # Isn't open for writing
                ValueError):   # Isn't open at all
            self._stream = sys.stdout
        else:
            self._stream = sys.stdout

    def __enter__(self):
        self.enable()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.disable()
            self._print_data()
            return True
        return False

    def _print_data(self):
        """Prints the results of the code profiling to the previously designated
        stream based on the previously designated sorting options.
        """

        ps = pstats.Stats(self, stream=self.stream).sort_stats(self.sortby)
        ps.print_stats()
