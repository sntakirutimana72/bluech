from .support.unittests import PyTestCase
from .support.declarations import RequestSpecs
from ..utils.validators import Validators as Val
from ..utils.interfaces import AttributeDict

class TestRequestValidator(PyTestCase):
    @classmethod
    def setup_class(cls):
        cls.request = RequestSpecs.for_validators()

    def test_with_minimal_expected_arguments(self):
        validated = Val.request(self.request)
        self.assert_isinstanceof(validated, dict)
        self.assert_isinstanceof(validated['request']['body'], AttributeDict)

    def test_without_body(self):
        req = {**self.request}
        del req['request']['body']
        validated = Val.request(req)

        self.assert_dict_has_key(validated, 'request')
        with self.assert_raises():
            self.assert_dict_has_key(validated['request'], 'body')

    def test_with_params(self):
        raw_req = {**self.request}
        raw_req['request']['params'] = {'id': 11}

        validated = Val.request(raw_req)
        self.assert_dict_has_key(validated, 'request')
        self.assert_isinstanceof(validated['request']['params'], AttributeDict)

    def test_without_request(self):
        raw = {**self.request}
        del raw['request']

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_request(self):
        raw = self.request.copy()
        raw['request'] = [4, 8]

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_params(self):
        raw = {**self.request}
        raw['request']['params'] = {5: 'hello'}

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_body(self):
        raw = {**self.request}
        raw['request']['body'] = 'INVALID BODY'

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_content_type(self):
        raw = self.request.copy()
        raw['content_type'] = 'INVALID CONTENT TYPE'

        with self.assert_raises():
            Val.request(raw)

    def test_without_content_type(self):
        raw = {**self.request}
        del raw['content_type']

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_content_length(self):
        raw = self.request.copy()
        raw['content_length'] = 17.5

        with self.assert_raises():
            Val.request(raw)

    def test_without_content_length(self):
        raw = {**self.request}
        del raw['content_length']

        with self.assert_raises():
            Val.request(raw)

    def test_with_invalid_protocol(self):
        raw = self.request.copy()
        raw['protocol'] = None

        with self.assert_raises():
            Val.request(raw)

    def test_without_protocol(self):
        raw = {**self.request}
        del raw['protocol']

        with self.assert_raises():
            Val.request(raw)

class TestSessionValidators(PyTestCase):
    def test_signin_with_valid_schema(self):
        signin = {'body': {'user': {'email': 'example@', 'password': '1234!'}}}
        validated = Val.signin(signin)

        self.assert_true(validated)
        self.assert_dict_has_key(validated, 'body')

    def test_signin_with_invalid_schema(self):
        signin = {'body': {'user': {'email': 'example@', 'password': '1234!'}}, 'params': {}}
        with self.assert_raises():
            Val.signin(signin)
        with self.assert_raises():
            Val.signin({'body': 'INVALID DATA STRUCTURE'})

# noinspection PyTypedDict
class TestUserValidators(PyTestCase):
    def _assert_for_all(self, obj):
        self.assert_isinstanceof(obj, dict)
        self.assert_dict_has_key(obj, 'body')
        self.assert_dict_has_key(obj['body'], 'user')
        self.assert_isinstanceof(obj['body']['user'], dict)

    def test_nickname_with_valid_schema(self):
        schema = {'body': {'user': {'nickname': 'NEW NICKNAME'}}}
        self._assert_for_all(Val.edit_username(schema))

    def test_nickname_with_invalid_schema(self):
        schema = {'body': {'nickname': 11}}
        with self.assert_raises():
            Val.edit_username(schema)

        schema['body'] = {'user': {'nickname': 26}}
        with self.assert_raises():
            Val.edit_username(schema)

# noinspection PyTypedDict
class TestMessageValidators(PyTestCase):
    @classmethod
    def setup_class(cls):
        cls.full_req = {
            'body': {
                'message': {
                    'recipient': 1,
                    'description': 'NEW_MESSAGE',
                    'reply_to': 1
                }
            }
        }

    def test_valid_new_message(self):
        validated = Val.new_message(self.full_req)
        self.assert_true(validated)
        with self.assert_raises(AssertionError):
            self.assert_dict_has_key(validated, 'params')

        # without :reply_to
        no_reply_to = self.full_req.copy()
        del no_reply_to['body']['message']['reply_to']
        validated = Val.new_message(no_reply_to)
        self.assert_isinstanceof(validated, dict)
        with self.assert_raises(AssertionError):
            self.assert_dict_has_key(validated['body']['message'], 'reply_to')

    def test_invalid_new_message(self):
        with_extra_key = {**self.full_req, 'params': 5}
        with self.assert_raises():
            Val.new_message(with_extra_key)

        invalid_recipient = self.full_req.copy()
        invalid_recipient['body']['message']['recipient'] = None
        with self.assert_raises():
            Val.new_message(invalid_recipient)

        del invalid_recipient['body']['message']['recipient']
        with self.assert_raises():
            Val.new_message(invalid_recipient)

        invalid_description = self.full_req.copy()
        invalid_description['body']['message']['description'] = 11
        with self.assert_raises():
            Val.new_message(invalid_description)

    def test_valid_edit_message(self):
        req = {
            'body': {'message': {'description': "EDIT MESSAGE"}},
            'params': {'id': 1}
        }
        validated = Val.edit_message(req)
        with self.assert_raises(AssertionError):
            self.assert_dict_has_key(validated['body']['message'], 'attachments')
        with self.assert_raises(AssertionError):
            self.assert_dict_has_key(validated['body']['message'], 'recipient')
        with self.assert_raises(AssertionError):
            self.assert_dict_has_key(validated['body']['message'], 'reply_to')

    def test_invalid_edit_message(self):
        with_extra_key = {
            'body': {'message': {'description': "EDIT MESSAGE", 'reply_to': 5}},
            'params': {'id': 1}
        }
        with self.assert_raises():
            Val.edit_message(with_extra_key)

        invalid_desc = {
            'body': {'message': {'description': ""}},
            'params': {'id': 1}
        }
        with self.assert_raises():
            Val.edit_message(invalid_desc)

        invalid_params = {
            'body': {'message': {'description': "EDITED"}},
            'params': {'id': None}
        }
        with self.assert_raises():
            Val.edit_message(invalid_params)

    def test_valid_remove_message(self):
        req = {
            'params': {'id': 1}
        }
        validated = Val.remove_message(req)
        self.assert_isinstanceof(validated, dict)
        self.assert_dict_has_key(validated, 'params')

    def test_invalid_remove_message(self):
        invalid_params = {'params': {}}
        with self.assert_raises():
            Val.remove_message(invalid_params)

    def test_valid_all_messages(self):
        req = {'params': {'recipient': 1}}
        Val.all_messages(req)

        req_with_page = req.copy()
        req_with_page['params']['page'] = 2
        Val.all_messages(req_with_page)

    def test_all_messages_with_body_prop(self):
        req = {'params': {'recipient': 1}, 'body': None}
        with self.assert_raises():
            Val.all_messages(req)

    def test_all_messages_with_invalid_recip(self):
        req = {'params': {'recipient': '11'}}
        with self.assert_raises():
            Val.all_messages(req)

    def test_all_messages_with_invalid_page(self):
        req = {'params': {'recipient': 1, 'page': 1.5}}
        with self.assert_raises():
            Val.all_messages(req)
