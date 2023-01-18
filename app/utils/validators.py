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
                Optional('params'): And({str: int}, Use(AttributeDict))
            }
        }).validate(req)
    
    # :Session
    #
    # :signin validator
    @staticmethod
    def signin(req): 
        return Schema({'body': {'name': str}}).validate(req)
        
    # :Users | :Groups
    #
    # :display_name validator, and it applies on both group and user factions
    @staticmethod
    def display_name(req): 
        return Schema({
            'body': {'display_name': str},
            'params': {'entity_id': int}
        }).validate(req)
    
    # :Users
    #
    # :all_users validator
    @staticmethod
    def edit_profile_pic(req):
        return Schema({
            'body': {'data': str},
            'params': {'user_id': int}
        }).validate(req)
   
    # :Groups
    #
    # :new_group validator
    @staticmethod
    def new_group(req):
        return Schema({
            'body': {
                'name': str,
                'created_by': int,
                'is_private': bool
            }
        }).validate(req)
        
    # :new_member validator
    @staticmethod
    def new_member(req):
        return Schema({
            'body': {
                'user_id': str,
                'is_group_admin': bool
            },
            'params': {'group_id': int}
        }).validate(req)
    
    # :new_member validator
    @staticmethod
    def remove_member(req):
        return Schema({
            'body': None,
            'params': {
                'group_id': int,
                'member_id': int
            }
        }).validate(req)
    
    # :exit_group & :remove_group validator
    @staticmethod
    def exit_or_remove_group(req):
        return Schema({
            'body': None,
            'params': {'group_id': int}
        }).validate(req)
    
    # :group_privilege validator
    @staticmethod
    def assign_group_privilege(req):
        return Schema({
            'body': {'is_group_admin': bool},
            'params': {
                'group_id': int,
                'member_id': int
            }
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
