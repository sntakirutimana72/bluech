from .serializers import compress
from .. import models

class Response:

    @staticmethod
    def _make(proto: str, **kwargs) -> bytes:
        return compress({'protocol': proto, **kwargs})

    # noinspection PyProtectedMember
    @classmethod
    def _as_resource(cls, proto: str, resource: models._Model):
        return cls._make(proto, **{resource.name: resource.as_json()})

    @classmethod
    def as_exc(cls, message):
        return cls._make('exception', message=message)

    @classmethod
    def as_signin_success(cls, user):
        return cls._as_resource('signin_success', user)

    @classmethod
    def as_signin_failure(cls, message: str):
        return cls._make('signin_failure', message=message)

    @classmethod
    def as_signout_success(cls):
        return cls._make('signout_success')

    @classmethod
    def as_signout_failure(cls, message=''):
        return cls._make('signout_failure', message=message)

    @classmethod
    def as_message(cls, message):
        return cls._as_resource('message', message)

    @classmethod
    def as_message_edited(cls, message):
        return cls._as_resource('message_edited', message)

    @classmethod
    def as_my_nickname_changed(cls, user):
        return cls._as_resource('my_nickname_changed', user)

    @classmethod
    def as_nickname_changed(cls, resource):
        return cls._as_resource('nickname_changed', resource)
