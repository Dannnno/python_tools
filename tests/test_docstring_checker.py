import importlib

from . import docstring_checker


class SampleClass(object):

    def __init__(self): pass

    def some_method(self): pass

    def _private_method(self): pass

    @classmethod
    def some_classmethod(cls): pass

    @classmethod
    def _private_classmethod(cls): pass

    @staticmethod
    def some_staticmethod(): pass

    @staticmethod
    def _private_staticmethod(): pass


def sample_function(): pass


def _private_function(): pass


class TestCheckClassDocstrings(object):

    def test_sample_class(self):
        need = docstring_checker.check_docstrings(SampleClass)
        assert need == {'SampleClass',
                        'some_classmethod',
                        'some_method',
                        'some_staticmethod'}

    def test_sample_class_private(self):
        need = docstring_checker.check_docstrings(
            SampleClass, ignore_private=False)
        assert need == {'SampleClass',
                        'some_classmethod',
                        'some_method',
                        'some_staticmethod',
                        '_private_method',
                        '_private_classmethod',
                        '_private_staticmethod'}

    def test_sample_class_magic(self):
        need = docstring_checker.check_docstrings(
            SampleClass, ignore_magic=False)
        assert need == {'SampleClass',
                        'some_classmethod',
                        'some_method',
                        'some_staticmethod',
                        '__init__'}

    def test_sample_class_private_magic(self):
        need = docstring_checker.check_docstrings(
            SampleClass, ignore_private=False, ignore_magic=False)
        assert need == {'SampleClass',
                        'some_classmethod',
                        'some_method',
                        'some_staticmethod',
                        '_private_method',
                        '_private_classmethod',
                        '_private_staticmethod',
                        '__init__'}


class TestFunctionDocstrings(object):

    def test_normal_function(self):
        need = docstring_checker.check_docstrings(sample_function)
        assert need == {'sample_function'}

    def test_private_function(self):
        need = docstring_checker.check_docstrings(_private_function)
        assert not need

    def test_private_function_with_flag(self):
        need = docstring_checker.check_docstrings(
            _private_function(), ignore_private=False)
        print need
        assert need == {'_private_function'}


class TestModuleDocstrings(object):

    @classmethod
    def setup_class(cls):
        from . import sample_module
        cls.module = sample_module

    def test_module_docstrings(self):
        need = docstring_checker.check_docstrings(self.module)
        print need
        assert need == {'tests.sample_module', 'A', 'f'}
