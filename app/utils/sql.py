from .exceptions import *
from ..settings import LOGGING_LEVELS
from ..models import *

def db_logger(**kwargs) -> int:
    return Log.create(**kwargs)

def signin(username) -> User:
    try:
        user = User.get(User.name == username)
    except:
        raise Unauthorized

    db_logger(action_id=LOGGING_LEVELS.LOGIN, done_by=user)
    return user

def signout(user_id):
    db_logger(logging_level=LOGGING_LEVELS.LOGOUT, done_by=user_id)

def new_message(user_id, **kwargs) -> int:
    try:
        message = Message.create(user=user_id, **kwargs)
    except:
        raise ActiveModelError

    db_logger(logging_level=LOGGING_LEVELS.MSG_NEW, done_by=user_id)
    return message.id

def all_messages(user_id, **kwargs):
    try:
        messages = Message.get(recipient=user_id, **kwargs).where(Message.status != 'DISABLED')
    except:
        raise ActiveModelError

    if not messages:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_ALL, done_by=user_id)
    return messages

def edit_message(user_id, **kwargs):
    try:
        message = Message.update(**kwargs).where(Message.sender == user_id)
    except:
        raise ActiveModelError

    if message is None:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_EDIT, done_by=user_id)
    return message.id

def remove_message(user_id, pk):
    try:
        cn = Message.delete().where(Message.sender == user_id and Message.id == pk and Message.status != 'DISABLED')
    except:
        raise ActiveModelError

    if cn is None:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_DEL, done_by=user_id)
