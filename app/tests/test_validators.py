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
        
    def test_without_request(self):
        raw = {**self.request}
        del raw['request']
        
        with self.assert_raises():
            V.request(raw)
            
    def test_with_invalid_request(self):
        raw = {**self.request}
        raw['request'] = [4, 8]
        
        with self.assert_raises():
            V.request(raw)
        
    def test_with_invalid_params(self):
        raw = {**self.request}
        raw['request']['params'] = {5: 'hello'}
        
        with self.assert_raises():
            V.request(raw)
            
    def test_with_invalid_body(self):
        raw = {**self.request}
        raw['request']['body'] = 'INVALID BODY'
        
        with self.assert_raises():
            V.request(raw)
            
    def test_without_body(self):
        raw = {**self.request}
        del raw['request']['body']
        
        with self.assert_raises():
            V.request(raw)
            
    def test_with_invalid_content_type(self):
        raw = {**self.request}
        raw['content_type'] = 'INVALID CONTENT TYPE'
        
        with self.assert_raises():
            V.request(raw)
            
    def test_without_content_type(self):
        raw = {**self.request}
        del raw['content_type']
        
        with self.assert_raises():
            V.request(raw)
            
    def test_with_invalid_content_length(self):
        raw = {**self.request}
        raw['content_length'] = 17.5
        
        with self.assert_raises():
            V.request(raw)
            
    def test_without_content_length(self):
        raw = {**self.request}
        del raw['content_length']
        
        with self.assert_raises():
            V.request(raw)
            
    def test_with_invalid_protocol(self):
        raw = {**self.request}
        raw['protocol'] = None
        
        with self.assert_raises():
            V.request(raw)
            
    def test_without_protocol(self):
        raw = {**self.request}
        del raw['protocol']
        
        with self.assert_raises():
            V.request(raw)

class TestSessionValidators(PyTestCase):
    
    def test_signin_with_valid_schema(self):
        signin = {'body': {'user': {'email': 'example@', 'password': '1234!'}}}
        validated = V.signin(signin)
        
        self.assert_true(validated)
        self.assert_dict_has_key(validated, 'body')
        
    def test_signin_with_invalid_schema(self):
        signin = {'body': {'user': {'email': 'example@', 'password': '1234!'}}, 'params': {}}
        with self.assert_raises():
            V.signin(signin)
        with self.assert_raises():
            V.signin({'body': 'INVALID DATA STRUCTURE'})

class TestUserValidators(PyTestCase):
    
    def _assert_for_all(self, obj):
        self.assert_isinstanceof(obj, dict)
        self.assert_dict_has_key(obj, 'body')
        self.assert_dict_has_key(obj['body'], 'user')
        self.assert_isinstanceof(obj['body']['user'], dict)
    
    def test_display_name_with_valid_schema(self):
        schema = {'body': {'user': {'display_name': 'NEW DISPLAY NAME'}}}
        self._assert_for_all(V.display_name(schema))
        
    def test_display_name_with_invalid_schema(self):
        schema = {'body': {'display_name': 11}}
        with self.assert_raises():
            V.display_name(schema)
            
        schema['body'] = {'user': {'display_name': 26}}
        with self.assert_raises():
            V.display_name(schema)
            
    def test_edit_profile_pic_with_valid_schema(self):
        schema = {'body': {'user': {'picture': 'kdasji392iotfpng80438q', 'extension': 'png'}}}
        self._assert_for_all(V.edit_profile_pic(schema))
        
    def test_edit_profile_pic_with_invalid_schema(self):
        # with :picture as anything else other than `string`
        schema = {'body': {'user': {'picture': 545465, 'extension': 'png'}}}
        with self.assert_raises():
            V.edit_profile_pic(schema)
        # with :extension as anything else other than `string`
        schema['body']['user'] = {'picture': '545465', 'extension': None}
        with self.assert_raises():
            V.edit_profile_pic(schema)
        # With an extra key that is not countered for
        schema['body']['user']['length'] = 66
        with self.assert_raises():
            V.edit_profile_pic(schema)

class TestGroupValidators(PyTestCase):
    
    def test_new_group_with_valid_schema(self):
        # with members
        schema = {'body': {'group': {'name': 'NEW GROUP', 'members': [{'id': 1, 'is_admin': False}]}}}
        self.assert_true(V.new_group(schema))
        # without members
        del schema['body']['group']['members']
        self.assert_true(V.new_group(schema))
        
    def test_new_group_with_invalid_schema(self):
        # with invalid :members
        schema = {'body': {'group': {'name': 'NEW GROUP', 'members': []}}}
        with self.assert_raises():
            V.new_group(schema)
        # with invalid :name
        schema['body']['group']['name'] = None
        with self.assert_raises():
            V.new_group(schema)
            
    def test_group_display_name_with_valid_schema(self):
        schema = {
            'body': {'group': {'display_name': 'NEW GROUP'}},
            'params': {'id': 1}
        }
        self.assert_true(V.group_display_name(schema))
        
    def test_group_display_name_with_invalid_schema(self):
        # with invalid :params
        schema = {'body': {'group': {'display_name': 'NEW GROUP', 'params': {'id': None}}}}
        with self.assert_raises():
            V.group_display_name(schema)
        # without :params
        del schema['body']['group']['params']
        with self.assert_raises():
            V.group_display_name(schema)
        # with invalid :dispaly_name
        schema['body']['group']['params'] = {'id': 'dsaee251fdsbgt4'}
        schema['body']['group']['display_name'] = 342432
        with self.assert_raises():
            V.group_display_name(schema)
        # without :display_name
        del schema['body']['group']['display_name']
        with self.assert_raises():
            V.group_display_name(schema)
            
    def test_new_member_with_valid_schema(self):
        # with members
        schema = {
            'body': {'group': {'members': [{'id': 1, 'is_admin': False}]}},
            'params': {'id': 'kopert9834534i'}
        }
        validated = V.new_member(schema)
        
        self.assert_true(validated)
        self.assert_isinstanceof(validated['body']['group']['members'], list)
        
    def test_new_member_with_invalid_schema(self):
        # with invalid :members
        schema = {
            'body': {'group': {'members': [{'id': 1, 'is_admin': 5}]}},
            'params': {'id': 'kopert9834534i'}
        }
        with self.assert_raises():
            V.new_group(schema)
        # with empty :members
        schema['body']['group']['members'] = []
        with self.assert_raises():
            V.new_group(schema)
        # without :members
        del schema['body']['group']['members']
        with self.assert_raises():
            V.new_group(schema)
        # with invalid :params
        schema['body']['group']['members'] = [{'id': 1, 'is_admin': False}, {'id': 2, 'is_admin': True}]
        schema['body']['group']['params'] = {'id': None}
        with self.assert_raises():
            V.new_group(schema)
        # without :params
        del schema['body']['group']['params']
        with self.assert_raises():
            V.new_group(schema)
            
    def test_valid_remove_member(self):
        schema = {
            'body': {'group': {'members': [11]}},
            'params': {'id': 'dksj438pjgD='}
        }
        validated = V.remove_member(schema)
        
        self.assert_true(validated)
        self.assert_isinstanceof(validated, dict)
        
    def test_invalid_remove_member(self):
        # invalid :members
        schema = {
            'body': {'group': {'members': ['11']}},
            'params': {'id': 'dksj438pjgD='}
        }
        with self.assert_raises():
            V.remove_member(schema)
        # invalid :members
        schema = {
            'body': {'group': {'members': ['11']}},
            'params': {'id': 'dksj438pjgD='}
        }
        with self.assert_raises():
            V.remove_member(schema)
