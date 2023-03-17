__all__ = (
    'SessionQueryManager',
    'MessageQueryManager',
    'UserQueryManager',
    'ChannelQueryManager',
)

import peewee as pee

from .exceptions import *
from ..models import *
from ..settings import LOGGING_LEVELS

class SQLQueryManager(object):
    @staticmethod
    def logger(level: int, **options):
        activity = Activity.get(Activity.level == level)
        ActivityLog.create(activity=activity, **options)

class SessionQueryManager(SQLQueryManager):
    @classmethod
    def signin(cls, email: str, password: str) -> User:
        try:
            user: User = User.get(User.email == email)
            user.authenticate(password)
        except:
            raise Unauthorized
        cls.logger(level=LOGGING_LEVELS.LOGIN, doer=user, summary='login')
        return user

    @classmethod
    def signout(cls, user_id: int):
        cls.logger(level=LOGGING_LEVELS.LOGOUT, doer=user_id, summary='logout')

class MessageQueryManager(SQLQueryManager):
    @classmethod
    def new_message(cls, **kwargs) -> int:
        try:
            message = Message.create(**kwargs)
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
    def edit_message(cls, sender: int, pk: int, **kwargs):
        try:
            cn = (Message
                  .update(**kwargs)
                  .where((Message.sender == sender) & (Message.id == pk))
                  .execute())
        except:
            raise ActiveRecordError
        if not cn:
            raise ResourceNotFound
        # cls.logger(LOGGING_LEVELS.MSG_EDIT, user_id)

    @classmethod
    def remove_message(cls, sender: int, pk: int) -> int | str:
        try:
            message = Message.get(Message.sender == sender, Message.id == pk)
            recipient_id = message.recipient.id
            message.delete_instance()
        except:
            raise ActiveRecordError
        # cls.logger(LOGGING_LEVELS.MSG_DEL, user_id)
        return recipient_id

class UserQueryManager(SQLQueryManager):
    @classmethod
    def edit_nickname(cls, pk: int, nickname: str):
        try:
            user: User = User.get_by_id(pk)
            if user.nickname == nickname:
                raise ResourceNotChanged
            user.nickname = nickname
            user.save()
        except ResourceNotChanged:
            raise ResourceNotChanged
        except:
            raise ActiveRecordError
        cls.logger(level=LOGGING_LEVELS.USER_EDIT_NICKNAME, doer=pk, summary='change user nickname')

    @classmethod
    def change_avatar(cls, pk: int):
        cls.logger(level=LOGGING_LEVELS.USER_EDIT_PIC, doer=pk, summary='change user avatar')

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
