"""I'm just messing with how I could indicate that all variables should
be made into properties (so no one has to type in all that cruft).

I don't think this is practical - there isn't really a point to using 
properties unless there is non-trivial logic for get/set/delete, and
non-trivial logic isn't something this can handle (or if it did it wouldn't
be readable, and that is sort of pointless.

Just an excercise
"""


import functools
import itertools
import types


def make_all_properties(class_):
    if isinstance(class_, types.InstanceType):
        raise TypeError(
                    "{} must be a class, not an instance".format(class_))
    if not isinstance(class_, (types.ClassType, type)):
        raise TypeError(
                    "{} must be a class, not a {}".format(class_, type(class_)))
    @functools.wraps(class_)
    def propertify(*args, **kwargs):
        #print class_, "Inside the wrapped class"
        d={}
        for truth, iterator in itertools.groupby(vars(class_).iteritems(), 
                                                 lambda x: 
                                                    isinstance(x[1], property)):
            if truth in d:
                d[truth].update(dict(list(iterator)))
            else:
                d[truth] = dict(list(iterator))
        #print d
        instance = class_(*args, **kwargs)
        return instance
    #print class_
    return propertify
    
    
class test_metaclass(type):
    
    @classmethod
    def __new__(cls, *args):
        properties = {}
        attributes = {}
        for k, v in args[-1].items():
            if not (k.startswith('__') or k.endswith('__')):
                if isinstance(v, property):
                    properties[k] = v
                else:
                    attributes[k] = v
        
        for key, attr in attributes.iteritems():
            if key.startswith('__'):
                pass
            elif key.startswith('_'):
                if key[1:] in properties:
                    pass
            else:
                if key in properties:
                    pass
                    
        print attributes
        print properties
        return super(test_metaclass, cls).__new__(*args)
    

@make_all_properties
class a(object):
    b=3
    _c=0
    
    
    __metaclass__ = test_metaclass
    
    def __init__(self):
        self.b = 6
        
    @property
    def c(self):
        return self._c
        
    @c.setter
    def c(self, other):
        self._c = other
        
a()