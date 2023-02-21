__all__ = (
    'MetaExtension',
    'ChannelExtension',
    'UserExtension',
    'MemberExtension',
    'MessageExtension',
    'ResourceExtension',
    'ActivityExtension',
    'ActivityLogExtension',
)

import datetime as dt

from ..policies.secure_password import PasswordHasherPolicy

class MetaExtension(object):
    @classmethod
    def cls_name(cls):
        return cls.__name__.lower()

    @property
    def name(self):
        return self.cls_name()

# noinspection PyAttributeOutsideInit
class Extension(object):
    def save(self, *args, **kwargs):
        if self._pk:
            self.updated_at = dt.datetime.now()
        return super(Extension, self).save(*args, **kwargs)

    @staticmethod
    def to_json():
        return [('id',)]

    @property
    def as_json(self):
        return {}

# noinspection PyAttributeOutsideInit
class UserExtension(Extension):
    def authenticate(self, password: str):
        assert PasswordHasherPolicy.verify(password, self.password)

    def save(self, *args, **kwargs):
        if self.is_dirty() and 'password' in self.dirty_fields:
            hashed_password = PasswordHasherPolicy.generate(self.password)
            self.password = hashed_password
        return super(UserExtension, self).save(*args, **kwargs)

class ChannelExtension(Extension):
    ...

class MessageExtension(Extension):
    ...

class MemberExtension(Extension):
    ...

class ResourceExtension(Extension):
    ...

class ActivityExtension(Extension):
    ...

class ActivityLogExtension(Extension):
    ...
