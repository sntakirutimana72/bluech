from ..utils.unittest.unittests import PyTestCase
from ..utils.validators import Validators as V
from ..utils.interfaces import AttributeDict
from ..settings import CONTENT_TYPES

class TestRequestValidator(PyTestCase):
    request = {
        'content_type': CONTENT_TYPES[0],
        'content_length': 343,
        'protocol': 'signin',
        'request': {
            'body': {
                'email': 'steve@email.com',
                'password': 'skafjoeuwitweuvjmepwiutlkg'
            }
        }
    }
    
    def test_with_minimal_expected_arguments(self):
        validated = V.request(self.request)
        self.assert_isinstanceof(validated, dict)
        self.assert_isinstanceof(validated['request']['body'], AttributeDict)
        
    def test_with_body_as_none(self):
        req = {**self.request}
        req['request']['body'] = None
        validated = V.request(req)
        
        self.assert_dict_has_key(validated, 'request')
        self.assert_is_none(validated['request']['body'])
        
    def test_with_params(self):
        raw_req = {**self.request}
        raw_req['request']['params'] = {'id': 11}
        
        validated = V.request(raw_req)
        self.assert_dict_has_key(validated, 'request')
        self.assert_isinstanceof(validated['request']['params'], AttributeDict)
        
    def test_with_wrong_params(self):
        raw = {**self.request}
        raw['request']['params'] = {5: 'hello'}
        
        with self.assert_raises():
            V.request(raw)
