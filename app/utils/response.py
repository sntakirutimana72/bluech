from .serializers import compress
from ..models import Message, Group

class Response:

    @staticmethod
    def _make(protocol, **kwargs):
        return compress({'protocol': protocol, ...kwargs})
        
    @classmethod
    def as_exc(cls, message):
        return cls._make('exception', message=message)
        
    @classmethod
    def as_signin_success(cls, user):
        return cls._make('signin_success', user=user.as_json())
        
    @classmethod
    def as_signin_failure(cls):
        return cls._make('signin_failure', message='401: Unauthorized')
        
    @classmethod
    def as_signout_success(cls):
        return cls._make('signout_success')
        
    @classmethod
    def as_signout_failure(cls, message=''):
        return cls._make('signout_failure', message=message)
        
    @classmethod
    def as_message(cls, message_id):
        message = Message.get_by_id(message_id)
        return cls._make('message', message=message.as_json())
        
    @classmethod
    def as_message_edited(cls, message_id):
        message = Message.get_by_id(message_id)
        return cls._make('message_edited', message=message.as_json())
        
    @classmethod
    def as_my_nickname_changed(cls, user):
        return cls._make('my_nickname_changed', message=message.as_json())
        
    @classmethod
    def as_nickname_changed(cls, entity_id, is_group=False):
        if is_group:
            entity = Group.get_by_id(entity_id)
        else:
            entity = User.get_by_id(entity_id)
        return cls._make('nickname_changed', message=message.as_json())
    