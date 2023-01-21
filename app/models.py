__all__ = (
    'User',
    'Channel',
    'Member',
    'Message',
    'Resource',
    'Activity',
    'ActivityLog',
)

from datetime import datetime
from uuid import uuid4
from peewee import (
    Model, DatabaseProxy, ForeignKeyField, CompositeKey,
    CharField, TextField, DateTimeField, BooleanField,
    UUIDField, ManyToManyField, DeferredThroughModel
)

from .utils.interfaces import AttributeDict

MembershipThroughModel = DeferredThroughModel()

class _Model(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = DatabaseProxy()

    def as_json(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__.lower()
    
class User(_Model):
    email = CharField(unique=True, max_length=100)
    password = CharField(null=False)
    nickname = CharField(max_length=12, null=False)

    def as_json(self):
        return AttributeDict({
            'id': self.id, 'nickname': self.nickname, 'photo': self.photo.to_json()
        })
        
class Channel(_Model):
    uuid = UUIDField(unique=True, default=uuid4)
    nickname = CharField(max_length=12, null=False)
    created_by = ForeignKeyField(User, backref='channels')
    members = ManyToManyField(User, backref='channels', through_model=MembershipThroughModel)
    
class Member(_Model):
    is_admin = BooleanField(default=False, null=False)
    is_creator = BooleanField(default=False, null=False)
    user = ForeignKeyField(User)
    channel = ForeignKeyField(Channel)

    class Meta:
        primary_key = CompositeKey('user', 'channel')
        
MembershipThroughModel.set_model(Member)
        
class Message(_Model):
    sender = ForeignKeyField(User, backref='messages')
    recipient = ForeignKeyField(User, backref='receipts')
    description = TextField()
    is_edited = BooleanField(default=False, null=False)
    reply_to = ForeignKeyField('self', backref='replies', null=True)
    
class Resource(_Model):
    name = CharField(max_length=60)
    path = CharField(unique=True)
    suffix = CharField(max_length=5)
    
    user = ForeignKeyField(User, backref='picture', null=True)
    channel = ForeignKeyField(Channel, backref='attachments', null=True)
    message = ForeignKeyField(Message, backref='attachments', null=True)
    
    def to_json(self):
        return AttributeDict({
            'name': self.name, 'path': self.path, 'suffix': self.suffix
        })

class Activity(_Model):
    name = CharField(unique=True, max_length=16)

class ActivityLog(_Model):
    summary = TextField()
    activity = ForeignKeyField(Activity, backref='logs')
    doer = ForeignKeyField(User, backref='logs')
