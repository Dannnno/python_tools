import inspect
import logging
import os
import sys
import types


logging.basicConfig(filename='logging.log', level=logging.DEBUG)


def check_docstrings(obj):
    if isinstance(obj, dict):
        iterator = obj.iteritems() 
    else:
        iterator = inspect.getmembers(obj)
        
    for _, value in iterator:
        if isinstance(value, types.FunctionType):
            if value.__doc__ is None:
                if not value.__name__.startswith('_'):
                    logging.info(value.__name__)
        elif isinstance(value, (type, types.ClassType)):
            if value.__doc__ is None:
                if not value.__name__.startswith('_'):
                    logging.info(value.__name__)
            for _, v in vars(value).iteritems():
                if isinstance(v, types.FunctionType):
                    if v.__doc__ is None:
                        if not value.__name__.startswith('_'):
                            logging.info(value.__name__)


def get_module(filepath):
    sys.path.insert(0, '')
    filepath = os.path.basename(os.path.abspath(filepath))
    original_directory = os.getcwd()
    try:
        path = os.path.dirname(filepath)        
        sys.path[0] = path
        filename, _, _ = filepath.partition('.')
        ret_module = __import__(filename)
    except ImportError:
        raise ImportError("No module {} at {}".format(filename, path))
    except WindowsError:
        pass
    else:
        return ret_module
    finally:
        os.chdir(original_directory)
        del sys.path[0]
        
        
def check_package_docstrings(package_dir):
    if os.path.isdir(package_dir):
        dir_name = os.path.abspath(package_dir)
    else:
        dir_name = os.path.dirname(os.path.abspath(package_dir))
        
    for file_ in os.listdir(dir_name):
        if not file_.startswith('.'):
            if os.path.isdir(file_):
                check_package_docstrings(file_)
            else:
                if file_.endswith('.py'):
                    logging.info(os.path.abspath(file_))
                    check_docstrings(get_module(file_))


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
                description="Checks docstrings of modules/packages")
    parser.add_argument('-f', '--filename', dest='filename',
                        default=__file__, help="name of the file to check")
    parser.add_argument('-p', '--package', dest='package',
                        default=False, action='store_true',
                        help="Check the whole package")       
    parser.add_argument('-l', '--logfile', dest='logfile',
                        default='logging.log', 
                        help="Name of the desired output log file")
                        
    args = parser.parse_args()
    
    logging.basicConfig(filename=args.logfile)
    if args.package:
        check_package_docstrings(
                os.path.dirname(os.path.abspath(args.filename)))
    else:
        check_docstrings(get_module(args.filename))
