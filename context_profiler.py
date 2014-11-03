try:
    import cProfile as Profile
except ImportError:
    import profile as Profile
finally:
    import pstats
    import sys

        
class context_profiler(Profile.Profile):
    
    def __init__(self, sortby='cumulative', stream=sys.stdout, **kwargs):
        super(context_profiler, self).__init__(**kwargs)
        self.sortby = sortby
        self.stream = stream
        
    def __enter__(self):
        self.enable()
        return self
        
    def __exit__(self, exc_type, exc_value, tback):
        if exc_type is None:
            self.disable()
            self.print_data()
            return True
        return False
            
    def print_data(self):
        ps = pstats.Stats(self, stream=self.stream).sort_stats(self.sortby)
        ps.print_stats()
        
        
if __name__ == '__main__':
    with open("C:/Users/Dan/Desktop/Programming/Python/my_file.txt", 'w') as f, \
          context_profiler(stream=f) as pr:
        for i in xrange(2):
            for j in range(10000):
                pr.stream.write(str(i+j))
                