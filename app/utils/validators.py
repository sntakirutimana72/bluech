from schema import Schema, Or, And, Use, Optional

from .interfaces import AttributeDict
from ..settings import CONTENT_TYPES

class Validators:
    @staticmethod
    def strict_content_types(raw_type: str):
        client_types = raw_type.replace(' ', '').split(';')
        for content_type in client_types:
            if content_type not in CONTENT_TYPES:
                return False
        return True

    # :default validator
    @classmethod
    def request(cls, req):
        return Schema({
            'content_type': cls.strict_content_types,
            'content_length': int,
            'protocol': str,
            'request': {
                Optional('body'): And({str: object}, Use(AttributeDict)),
                Optional('params'): And({str: Or(int, str)}, Use(AttributeDict))
            }
        }).validate(req)

    # :Session
    #
    # :signin validator
    @staticmethod
    def signin(req):
        return Schema({'body': {'user': {'email': str, 'password': str}}}).validate(req)

    # :Users
    #
    # :nickname validator
    @staticmethod
    def edit_username(req):
        return Schema({'body': {'user': {'nickname': str}}}).validate(req)

    # :Messages
    #
    # :new_message validator
    @staticmethod
    def new_message(req):
        return Schema({
            'body': {
                'message': {
                    'recipient': Or(int, str),
                    Optional('description'): And(str, len),
                    Optional('reply_to'): int
                }
            }
        }).validate(req)

    # :edit_message validator
    @staticmethod
    def edit_message(req):
        return Schema({
            'body': {'message': {'description': And(str, len)}},
            'params': {'id': int}
        }).validate(req)

    # :remove_message validator
    @staticmethod
    def remove_message(req):
        return Schema({'params': {'id': int}}).validate(req)

    @staticmethod
    def all_messages(req):
        return Schema({
            'params': {'recipient': int, Optional('page'): int}
        }).validate(req)
