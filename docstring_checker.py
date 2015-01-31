"""This module servers to locate and identify pyhon modules, classes, and
functions that do not currently have docstrings.
"""

import inspect
import importlib
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


def get_module(module_name, package=None, path=None):
    """Gets a python module from a specific location.

    Parameters
    ----------
    module_name : string
        The name of the module to be imported
    package : string, optional
        The package from which the module should be imported
    path : string, optional
        The path to the package/module, assuming that the package/module is not
        already on sys.path.

    Returns
    -------
    module
        The python module that was imported by `importlib.import_module`

    Raises
    ------
    ImportError
        Raised when some part of the import process fails.  Generally caused by
        an error with the path or package.

    Notes
    -----
    This function is a wrapper for the `importlib.import_module` function that
    adds support for adjusting sys.path.  Errors can likely be resolved by
    examining the documentation[1]_ for that function.

    .. [1][https://docs.python.org/2.7/library/importlib.html]
    """

    if path is not None:
        sys.path.insert(0, path)

    return importlib.import_module(module_name, package=package)
