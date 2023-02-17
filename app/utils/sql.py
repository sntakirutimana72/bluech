__all__ = (
    'SessionQueryManager',
    'MessageQueryManager',
    'UserQueryManager',
    'ChannelQueryManager',
)

from .exceptions import *
from ..settings import LOGGING_LEVELS
from ..models import *

class SQLQueryManager(object):
    @staticmethod
    def _logging(**options):
        return ActivityLog.create(**options)

class SessionQueryManager(SQLQueryManager):
    @classmethod
    def signin(cls, email, password) -> User:
        try:
            user: User = User.get(User.email == email)
            user.authenticate(password)
        except:
            raise Unauthorized

        cls._logging(action_id=LOGGING_LEVELS.LOGIN, done_by=user)
        return user
    
    @classmethod
    def signout(cls, user_id: int):
        cls._logging(logging_level=LOGGING_LEVELS.LOGOUT, done_by=user_id)

class MessageQueryManager(SQLQueryManager):
    @classmethod
    def new_message(cls, user_id: int, **kwargs) -> int:
        try:
            message = Message.create(user=user_id, **kwargs)
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.MSG_NEW, done_by=user_id)
        return message.id

    @classmethod
    def all_messages(cls, user_id: int, **kwargs):
        try:
            messages = Message.get(recipient=user_id, **kwargs).where(Message.status != 'DISABLED')
        except:
            raise ActiveModelError

        if not messages:
            raise NoResourcesFound

        cls._logging(logging_level=LOGGING_LEVELS.MSG_ALL, done_by=user_id)
        return messages

    @classmethod
    def edit_message(cls, user_id: int, pk: int, **kwargs):
        try:
            cn = Message.update(**kwargs).where(Message.sender == user_id and Message.id == pk)
        except:
            raise ActiveModelError

        if cn is None:
            raise NoResourcesFound

        cls._logging(logging_level=LOGGING_LEVELS.MSG_EDIT, done_by=user_id)

    @classmethod
    def remove_message(cls, user_id: int, pk: int):
        try:
            cn = Message.delete().where(Message.sender == user_id and Message.id == pk and Message.status != 'DELETED')
        except:
            raise ActiveModelError

        if cn is None:
            raise NoResourcesFound

        cls._logging(logging_level=LOGGING_LEVELS.MSG_DEL, done_by=user_id)

class UserQueryManager(SQLQueryManager):
    @classmethod
    def edit_user_display_name(cls, pk: int, display_name: str):
        try:
            user: User = User.get_by_id(pk)
            if user.display_name == display_name:
                raise ResourceNotChanged

            user.display_name = display_name
            user.save()
        except ResourceNotChanged as ex:
            raise ex
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.USER_EDIT_MAME, done_by=pk)

    @classmethod
    def edit_user_profile_picture(cls, pk: int, data: bytes, extension: str):
        with open(f'{pk!r}-user-profile-picture.{extension!r}', 'rb') as fd:
            fd.write(data)
            fd.flush()
        cls._logging(logging_level=LOGGING_LEVELS.USER_EDIT_PIC, done_by=pk)

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
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.USERS_ALL, done_by=pk)
        return users + list(channels)

class ChannelQueryManager(SQLQueryManager):
    @classmethod
    def new_channel(cls, user_id: int, **kwargs):
        try:
            channel = Channel.create(created_by=user_id, **kwargs)
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.CHANNEL_NEW, done_by=user_id)
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
            raise ActiveModelError

        if not results:
            raise Unauthorized

        member = Member.create(channel=pk, **kwargs)
        cls._logging(logging_level=LOGGING_LEVELS.MEMBER_ADD, done_by=user_id)
        return member.as_json()

    @classmethod
    def remove_member(cls, user_id: int, member_id: int, channel_id: int):
        try:
            if user_id == member_id:
                raise

            admin: Member | None = Member.get(Member.user == user_id, Member.channel == channel_id, Member.is_channel_admin)
            if admin is None:
                raise

            member: Member | None = Member.get(Member.user == member_id, Member.channel == channel_id)
            if member is None:
                raise
            member.delete_instance()
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.MEMBER_DEL, done_by=user_id)

    @classmethod
    def exit_channel(cls, member_id: int, channel_id: int):
        try:
            member: Member | None = Member.get(Member.user == member_id, Member.channel == channel_id)
            if member is None or member.is_founder:
                raise
            member.delete_instance()
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.CHANNEL_EXIT, done_by=member_id)

    @classmethod
    def delete_channel(cls, user_id: int, channel_id: int):
        try:
            channel: Channel | None = Channel.get(Channel.id == channel_id, Channel.created_by == user_id)
            if channel is None:
                raise
            channel.delete_instance()
        except:
            raise ActiveModelError

        cls._logging(logging_level=LOGGING_LEVELS.CHANNEL_DEL, done_by=user_id)
