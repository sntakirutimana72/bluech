__all__ = (
    'SessionQueryManager',
    'MessageQueryManager',
    'UserQueryManager',
    'ChannelQueryManager',
)

import peewee as pee

from .exceptions import *
from ..settings import LOGGING_LEVELS
from ..models import *

class SQLQueryManager(object):
    @staticmethod
    def logger(level: int, doer: int | User, **options):
        activity = Activity.get(Activity.level == level)
        return ActivityLog.create(activity=activity, doer=doer, **options)

class SessionQueryManager(SQLQueryManager):
    @classmethod
    def signin(cls, email: str, password: str) -> User:
        try:
            user: User = User.get(User.email == email)
            user.authenticate(password)
        except:
            raise Unauthorized
        # cls.logger(LOGGING_LEVELS.LOGIN, user)
        return user

    @classmethod
    def signout(cls, user_id: int):
        # cls.logger(LOGGING_LEVELS.LOGOUT, user_id)
        ...

class MessageQueryManager(SQLQueryManager):
    @classmethod
    def new_message(cls, user_id: int, **kwargs) -> int:
        try:
            message = Message.create(user=user_id, **kwargs)
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.MSG_NEW, user_id)
        return message.id

    @classmethod
    def all_messages(cls, user_id: int, **kwargs):
        try:
            messages = Message.get(recipient=user_id, **kwargs).where(Message.status != 'DISABLED')
        except pee.DoesNotExist:
            raise ResourceNotFound
        except:
            raise ActiveRecordError
        if not messages:
            raise ResourceNotFound
        # cls.logger(LOGGING_LEVELS.MSG_ALL, user_id)
        return messages

    @classmethod
    def edit_message(cls, user_id: int, pk: int, **kwargs):
        try:
            cn = Message.update(**kwargs).where(Message.sender == user_id and Message.id == pk)
        except:
            raise ActiveRecordError
        if cn is None:
            raise ResourceNotFound
        # cls.logger(LOGGING_LEVELS.MSG_EDIT, user_id)

    @classmethod
    def remove_message(cls, user_id: int, pk: int):
        try:
            cn = Message.delete().where(Message.sender == user_id and Message.id == pk and Message.status != 'DELETED')
        except:
            raise ActiveRecordError
        if cn is None:
            raise ResourceNotFound
        # cls.logger(LOGGING_LEVELS.MSG_DEL, user_id)

class UserQueryManager(SQLQueryManager):
    @staticmethod
    def edit_nickname(pk: int, nickname: str):
        try:
            user: User = User.get_by_id(pk)
            if user.nickname == nickname:
                raise ResourceNotChanged
            user.nickname = nickname
            user.save()
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.USER_EDIT_MAME, pk)

    @classmethod
    def change_avatar(cls, pk: int):
        # cls.logger(LOGGING_LEVELS.USER_EDIT_PIC, pk)
        ...  # simply the action since the user avatar has already persisted while in dowload

    @classmethod
    def all_users(cls, pk: int):
        try:
            users = User.select().where(User.id != pk)
            channels = (Channel
                        .select()
                        .join(User)
                        .switch(Channel)
                        .join(Member)
                        .where(Channel.created_by == pk or Member.channel == Channel and Member.user == pk))
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.USERS_ALL, pk)
        return users + list(channels)

class ChannelQueryManager(SQLQueryManager):
    @classmethod
    def new_channel(cls, user_id: int, **kwargs):
        try:
            channel = Channel.create(created_by=user_id, **kwargs)
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.CHANNEL_NEW, user_id)
        return channel.id

    @classmethod
    def new_member(cls, user_id: int, pk: int, **kwargs):
        try:
            query = (Channel
                     .select()
                     .join(User)
                     .switch(Channel)
                     .join(Member)
                     .where(Channel.id == pk,
                            Channel.created_by == user_id or (Member.user == user_id and Member.is_channel_admin)))
            results = list(query)
        except:
            raise ActiveRecordError
        if not results:
            raise Unauthorized
        member = Member.create(channel=pk, **kwargs)
        # cls.logger(LOGGING_LEVELS.MEMBER_ADD, user_id)
        return member.as_json()

    @classmethod
    def remove_member(cls, user_id: int, member_id: int, channel_id: int):
        try:
            if user_id == member_id:
                raise

            admin: Member | None = Member.get(Member.user == user_id, Member.channel == channel_id,
                                              Member.is_channel_admin)
            if admin is None:
                raise

            member: Member | None = Member.get(Member.user == member_id, Member.channel == channel_id)
            if member is None:
                raise
            member.delete_instance()
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.MEMBER_DEL, user_id)

    @classmethod
    def exit_channel(cls, member_id: int, channel_id: int):
        try:
            member: Member | None = Member.get(Member.user == member_id, Member.channel == channel_id)
            if member is None or member.is_founder:
                raise
            member.delete_instance()
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.CHANNEL_EXIT, member_id)

    @classmethod
    def delete_channel(cls, user_id: int, channel_id: int):
        try:
            channel: Channel | None = Channel.get(Channel.id == channel_id, Channel.created_by == user_id)
            if channel is None:
                raise
            channel.delete_instance()
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.CHANNEL_DEL, user_id)
