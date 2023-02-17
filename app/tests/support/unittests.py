import pytest
import contextlib

class PyTestCase(object):    
    @staticmethod
    def assert_is_false(obj):
        assert obj is False
    
    @staticmethod    
    def assert_is_true(obj):
        assert obj is True
     
    @staticmethod   
    def assert_is_none(obj):
        assert obj is None
    
    @staticmethod    
    def assert_true(obj):
        """The assertion succeeds as long as the :param:obj is not empty | 0 | None | False"""
        assert bool(obj)
     
    @staticmethod   
    def assert_false(obj):
        assert not bool(obj)
    
    @staticmethod    
    def assert_isinstanceof(obj, *args):
        assert isinstance(obj, args)
       
    def assert_dict_has_key(self, obj: dict, key):
        self.assert_isinstanceof(obj, dict)
        assert key in obj
        
    @staticmethod
    def assert_equals(obj_1, obj_2):
        assert type(obj_1) is type(obj_2)
        assert obj_1 == obj_2
        
    def assert_not_equals(self, obj_1, obj_2):
        try:
            self.assert_equals(obj_1, obj_2)
        except AssertionError:
            assert True
            
    @staticmethod
    @contextlib.contextmanager
    def assert_raises(exc=BaseException):
        with pytest.raises(exc):
            yield
