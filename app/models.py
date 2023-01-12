__all__ = (
    'User',
    'Privilege',
    'UserPrivilege',
    'Action',
    'Resource',
    'Message',
    'Group',
    'Joint',
    'Log',
)

from datetime import datetime
from peewee import (
    Model, DatabaseProxy, ForeignKeyField, CompositeKey,
    CharField, TextField, DateTimeField, BooleanField
)

from .utils.interfaces import AttributeDict

class _Model(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    class Meta:
        database = DatabaseProxy()
        
    def as_json(self):
        return {}

class User(_Model):
    name = CharField(max_length=60)
    display_name = CharField(unique=True, max_length=12)
    
    def as_json(self):
        return AttributeDict({'id': self.id, 'display_name': self.display_name})

class Privilege(_Model):
    name = CharField(unique=True, max_length=16)
    description = TextField(null=True)

class UserPrivilege(_Model):
    assignee = ForeignKeyField(User, backref='created_rights', null=True)
    user = ForeignKeyField(User, backref='rights')
    privilege = ForeignKeyField(Privilege, backref='copywrites')

    class Meta(_Model.Meta):
        primary_key = CompositeKey('user_id', 'privilege_id')
        db_table = 'user_privileges'

class Action(_Model):
    name = CharField(unique=True, max_length=24)

class Message(_Model):
    description = TextField()
    is_delivered = BooleanField(default=False)
    is_edited = BooleanField(default=False)
    reply_to = ForeignKeyField('self', backref='replies', null=True)
    sender = ForeignKeyField(User, backref='messages')
    recipient = ForeignKeyField(User, backref='recipients')

class Resource(_Model):
    res_path = TextField()
    user = ForeignKeyField(User, backref='owners')
    message = ForeignKeyField(Message, backref='owners')

class Group(_Model):
    name = CharField(max_length=16)
    is_private = BooleanField(default=True)
    created_by = ForeignKeyField(User, backref='groups')

class Joint(_Model):
    is_group_admin = BooleanField(default=False)
    user = ForeignKeyField(User, backref='joints')
    group = ForeignKeyField(Group, backref='joints')

    class Meta(_Model.Meta):
        primary_key = CompositeKey('user_id', 'group_id')

class Log(_Model):
    summary = TextField()
    action = ForeignKeyField(Action, backref='logs')
    done_by = ForeignKeyField(User, backref='logs')
    # reference_to = ForeignKeyField(User, backref='references')
