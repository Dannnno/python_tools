import inspect
import os
import sys
import types


"""
I need to add docstrings here...
I need to check for private (_ prefixed) methods
I need to be able to import everything from a directory too...
"""


def check_docstrings(obj):
    for key, value in obj.items():
            if isinstance(value, types.FunctionType):
                if value.__doc__ is None:
                    yield value.__name__
            elif inspect.isclass(value):
                for k, v in value.__dict__.items():
                    if isinstance(v, types.FunctionType):
                        if v.__doc__ is None:
                            yield "{}.{}".format(key, v.__name__)
                            
                            
def get_module(filepath):
    original_directory = os.getcwd()
    try:
        path = os.path.dirname(filepath)
        filename, _, _ = os.path.basename(filepath).partition('.')
        os.chdir(path)
        ret_module = __import__(filename)
    except ImportError:
        raise ImportError("No module {} at {}".format(filename, path))
    except WindowsError:
        pass
    else:
        return ret_module
    finally:
        os.chdir(original_directory)
        
        
if __name__ == '__main__':
    print list(check_docstrings(globals()))
    print list(check_docstrings(get_module(r"C:\Users\Dan\Desktop\Programming\GitHub\Chemistry\CheML").__dict__))
    