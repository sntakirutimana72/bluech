__all__ = (
    'User',
    'Message',
    'Activity',
    'ActivityLog',
    '_Model'
)

import datetime as dt
import peewee as pee

from app.extensions.models import *

class _Model(MetaExtension, pee.Model):
    created_at = pee.DateTimeField(default=dt.datetime.now)
    updated_at = pee.DateTimeField(null=True)

    class Meta:
        database = pee.DatabaseProxy()

class User(UserExtension, _Model):
    email = pee.CharField(unique=True, max_length=100)
    password = pee.CharField(null=False)
    nickname = pee.CharField(max_length=12, null=False)

class Message(MessageExtension, _Model):
    sender = pee.ForeignKeyField(User, backref='messages')
    recipient = pee.ForeignKeyField(User, backref='receipts')
    description = pee.TextField(null=True)
    is_edited = pee.BooleanField(default=False)
    reply_to = pee.ForeignKeyField('self', backref='replies', null=True)

class Activity(ActivityExtension, _Model):
    level = pee.IntegerField(unique=True)

class ActivityLog(ActivityLogExtension, _Model):
    summary = pee.TextField()
    activity = pee.ForeignKeyField(Activity, backref='logs')
    doer = pee.ForeignKeyField(User, null=True, backref='activities')
