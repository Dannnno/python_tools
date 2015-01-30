import inspect
import importlib
import os
import sys


def _get_iterator(obj):
    """Returns the appropriate iterator, depending on the type of the object.

    Parameters
    ----------
    obj : Object
        The object whose iterator is going to be used

    Returns
    -------
    iterator : Iterable
        The iterable to be iterated over.  Will be in a format that supports
        the following for loop:

            for a, b in iterator:
                # Do something

    """

    if inspect.ismodule(obj):
        iterator = []
        [iterator.extend(inspect.getmembers(members))
         for members in inspect.getmembers(obj)]
        return iterator
    else:
        return inspect.getmembers(obj)


def check_docstrings(obj, ignore_private=True, ignore_magic=True,):
    """Checks if an object has the necessary docstrings.

    If the object is a module or a class then it will perform some introspection
    and check the members of that module or class.

    Parameters
    ----------
    obj : Object
        The object to be checked.
    ignore_private : bool, optional
        Indicates whether or not private functions (pre-fixed with a single
        underscore '_'), methods, classes, etc should be ignored.  Enabled by
        default.
    ignore_magic : bool, optional
        Indicates whether or not python magic attributes (pre- and post-fixed
        with double underscores '__') should be ignored.  Enabled by default.

    Returns
    -------
    need_docstrings : set
        A set of functions, methods, and classes (meeting provided filtering
        parameters) that do not currently have docstrings.

    """

    def _name_passes_filter(var_name):
        """Determines whether or not the name meets the filtering requirements
        specified by the keyword arguments to `check_docstrings`.

        Parameters
        ----------
        var_name : string
           The name that is being checked.

        Returns
        -------
        bool
            Whether or not the name meets the filtering requirements.
        """

        private = var_name.startswith('_') and not var_name.startswith('__')
        magic = var_name.startswith('__') and var_name.endswith('__')

        if ignore_magic and ignore_private:
            return not (magic or private)
        elif ignore_magic:
            return not magic
        elif ignore_private:
            return not private
        return True

    iterator = _get_iterator(obj)

    need_docstrings = []

    if hasattr(obj, '__doc__'):
        if obj.__doc__ is None or not obj.__doc__.strip():
            if hasattr(obj, '__name__'):
                if _name_passes_filter(obj.__name__):
                    need_docstrings.append(obj.__name__)
        
    for _, value in iterator:
        if hasattr(value, '__doc__'):
            docstring = value.__doc__
            if docstring is None or not docstring.strip():
                name = getattr(value, '__name__', None)
                if name is not None:
                    if _name_passes_filter(name):
                        need_docstrings.append(name)

    return set(need_docstrings)


def get_module(filepath):
    sys.path.insert(0, '')
    filepath = os.path.basename(os.path.abspath(filepath))
    original_directory = os.getcwd()
    try:
        path = os.path.dirname(filepath)
        sys.path[0] = path
        filename, _, _ = filepath.partition('.')
    except (WindowsError, IOError) as e:
        return
    else:
        try:
            ret_module = __import__(filename)
        except ImportError:
            raise ImportError("No module {} at {}".format(filename, path))
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
