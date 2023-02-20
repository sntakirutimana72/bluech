__all__ = (
    'User',
    'Channel',
    'Member',
    'Message',
    'Resource',
    'Activity',
    'ActivityLog',
    '_Model'
)

import datetime as dt
import uuid as u4
import peewee as pee

from app.extensions.models import *

MembershipThroughModel = pee.DeferredThroughModel()

class _Model(pee.Model):
    created_at = pee.DateTimeField(default=dt.datetime.now)
    updated_at = pee.DateTimeField(null=True)

    class Meta:
        database = pee.DatabaseProxy()

class User(UserExtension, _Model):
    email = pee.CharField(unique=True, max_length=100)
    password = pee.CharField(null=False)
    nickname = pee.CharField(max_length=12, null=False)

class Channel(ChannelExtension, _Model):
    uuid = pee.UUIDField(unique=True, default=u4.uuid4)
    nickname = pee.CharField(max_length=12)
    created_by = pee.ForeignKeyField(User, backref='channels')
    members = pee.ManyToManyField(User, backref='channels', through_model=MembershipThroughModel)

class Member(MemberExtension, _Model):
    is_admin = pee.BooleanField(default=False)
    is_creator = pee.BooleanField(default=False)
    user = pee.ForeignKeyField(User)
    channel = pee.ForeignKeyField(Channel)

    class Meta:
        primary_key = pee.CompositeKey('user', 'channel')

MembershipThroughModel.set_model(Member)

class Message(MessageExtension, _Model):
    sender = pee.ForeignKeyField(User, backref='messages')
    recipient = pee.ForeignKeyField(User, backref='receipts')
    description = pee.TextField(null=True)
    is_edited = pee.BooleanField(default=False)
    has_attachments = pee.BooleanField(default=False)
    reply_to = pee.ForeignKeyField('self', backref='replies', null=True)

class Resource(ResourceExtension, _Model):
    location = pee.CharField(unique=True)
    user = pee.ForeignKeyField(User, backref='picture', null=True)
    channel = pee.ForeignKeyField(Channel, backref='attachments', null=True)
    message = pee.ForeignKeyField(Message, backref='attachments', null=True)

class Activity(ActivityExtension, _Model):
    name = pee.CharField(unique=True, max_length=16)

class ActivityLog(ActivityLogExtension, _Model):
    summary = pee.TextField()
    activity = pee.ForeignKeyField(Activity, backref='logs')
    doer = pee.ForeignKeyField(User, backref='logs')
