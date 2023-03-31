__all__ = (
    'SessionQueryManager',
    'MessageQueryManager',
    'UserQueryManager',
)

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
        cls.logger(LOGGING_LEVELS.LOGIN, doer=user, summary='login')
        return user

    @classmethod
    def signout(cls, current_user: int):
        cls.logger(LOGGING_LEVELS.LOGOUT, doer=current_user, summary='logout')

class MessageQueryManager(SQLQueryManager):
    @classmethod
    def new_message(cls, **kwargs) -> int:
        try:
            message = Message.create(**kwargs)
        except:
            raise ActiveRecordError
        cls.logger(LOGGING_LEVELS.MSG_NEW, doer=kwargs['sender'], summary='New Message')
        return message.id

    @classmethod
    def all_messages(cls, current_user: int, recipient: int, page: int):
        try:
            query = (Message
                     .select()
                     .where(
                        ((Message.sender == current_user) & (Message.recipient == recipient))
                        |
                        ((Message.sender == recipient) & (Message.recipient == current_user))
                     )
                     .order_by(Message.created_at.desc())
                     .paginate(page, 25))
        except:
            raise ActiveRecordError
        cls.logger(LOGGING_LEVELS.MSG_ALL, doer=current_user, summary='Get all messages')
        return query

    @classmethod
    def edit_message(cls, current_user: int, pk: int, **kwargs):
        try:
            cn = (Message
                  .update(**kwargs)
                  .where((Message.sender == current_user) & (Message.id == pk))
                  .execute())
        except:
            raise ActiveRecordError
        if not cn:
            raise ResourceNotFound
        cls.logger(LOGGING_LEVELS.MSG_EDIT, doer=current_user, summary='Edit message')

    @classmethod
    def remove_message(cls, current_user: int, pk: int) -> int | str:
        try:
            message = Message.get(Message.sender == current_user, Message.id == pk)
            recipient_id = message.recipient.id
            message.delete_instance()
        except:
            raise ActiveRecordError
        cls.logger(LOGGING_LEVELS.MSG_DEL, doer=current_user, summary='Remove message')
        return recipient_id

class UserQueryManager(SQLQueryManager):
    @classmethod
    def edit_nickname(cls, current_user: int, nickname: str):
        try:
            user: User = User.get_by_id(current_user)
            if user.nickname == nickname:
                raise ResourceNotChanged
            user.nickname = nickname
            user.save()
        except ResourceNotChanged:
            raise ResourceNotChanged
        except:
            raise ActiveRecordError
        cls.logger(LOGGING_LEVELS.USER_EDIT_NICKNAME, doer=current_user, summary='change user nickname')

    @classmethod
    def change_avatar(cls, current_user: int):
        cls.logger(LOGGING_LEVELS.USER_EDIT_PIC, doer=current_user, summary='change user avatar')

    @classmethod
    def all_users(cls, current_user: int, ids):
        try:
            query = User.select().where(User.id << ids)
        except:
            raise ActiveRecordError
        cls.logger(LOGGING_LEVELS.USERS_ALL, doer=current_user, summary='Get all users')
        return query
