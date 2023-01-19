from schema import Schema, Or, And, Use, Optional

from .interfaces import AttributeDict
from ..settings import CONTENT_TYPES

class Validators:

    @staticmethod
    def enum_type(*enums):
        def validate(initial):
            return initial in enums
        return validate

    # :default validator
    @classmethod
    def request(cls, req): 
        return Schema({
            'content_type': cls.enum_type(*CONTENT_TYPES),
            'content_length': int,
            'protocol': str,
            'request': {
                'body': Or(None, And({str: object}, Use(AttributeDict))),
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
    # :display_name validator
    @staticmethod
    def display_name(req): 
        return Schema({'body': {'user': {'display_name': str}}}).validate(req)
    
    # :Users
    #
    # :all_users validator
    @staticmethod
    def edit_profile_pic(req):
        return Schema({'body': {'user': {'picture': str, 'extension': str}}}).validate(req)
   
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
                'recipient_id': int,
                'description': str,
                Optional('reply_to'): int
            }
        }).validate(req)
    
    # :edit_message validator
    @staticmethod
    def edit_message(req):
        return Schema({
            'body': {'description': str},
            'params': {'message_id': int}
        }).validate(req)
    
    # :remove_message validator
    @staticmethod
    def remove_message(req):
        return Schema({'params': {'message_id': int}}).validate(req)
