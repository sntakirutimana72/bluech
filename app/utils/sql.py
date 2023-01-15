from typing import Union

from .exceptions import Unauthorized
from ..models import User, Log
from ..settings import LOGGING_LEVELS

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
    db_logger(action_id=LOGGING_LEVELS.LOGOUT, done_by=user_id)

def change_user_display_name(username, display_name) -> Union[int, None]:
    user = User.get_or_none(User.name == username)
    if user is None:
        return
    if user.display_name == display_name or User.get_or_none(User.display_name == display_name):
        return
    user.display_name = display_name
    user.save()

    return user.id
