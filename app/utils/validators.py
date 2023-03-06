from schema import Schema, Or, And, Use, Optional

from .interfaces import AttributeDict
from ..settings import CONTENT_TYPES

class Validators:
    @staticmethod
    def strict_content_types(raw_type: str):
        client_types = raw_type.replace(' ', '').rstrip(';')
        if not (CONTENT_TYPES[0] in client_types and CONTENT_TYPES[1] in client_types):
            return False
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

    # :Groups
    #
    # :new_group validator
    @staticmethod
    def new_group(req):
        return Schema({
            'body': {
                'group': {
                    'name': str,
                    Optional('members'): And([{'id': int, 'is_admin': bool}], len)
                }
            }
        }).validate(req)

    # :group_display_name validator
    @staticmethod
    def group_display_name(req):
        return Schema({
            'body': {'group': {'display_name': str}},
            'params': {'id': Or(int, str)}
        }).validate(req)

    # :new_member validator
    @staticmethod
    def new_member(req):
        return Schema({
            'body': {'group': {'members': And([{'id': int, 'is_admin': bool}], len)}},
            'params': {'id': Or(int, str)}
        }).validate(req)

    # :new_member validator
    @staticmethod
    def remove_member(req):
        return Schema({
            'body': {'group': {'members': And([int], len)}},
            'params': {'id': Or(int, str)}
        }).validate(req)

    # :exit_group & :remove_group validator
    @staticmethod
    def exit_or_remove_group(req):
        return Schema({
            'body': None,
            'params': {'id': Or(int, str)}
        }).validate(req)

    # :group_privilege validator
    @staticmethod
    def assign_group_privilege(req):
        return Schema({
            'body': {'group': {'member': {'id': int, 'is_admin': bool}}},
            'params': {'id': Or(int, str)}
        }).validate(req)

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
                    Optional('reply_to'): int,
                    Optional('attachments'): And([{'media': str, 'name': str, 'suffix': str}], len)
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
        return Schema({'body': None, 'params': {'id': int}}).validate(req)
