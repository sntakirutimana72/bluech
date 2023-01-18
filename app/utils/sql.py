from .exceptions import *
from ..settings import LOGGING_LEVELS
from ..models import *

def db_logger(**kwargs) -> int:
    return Log.create(**kwargs)

def signin(username: str) -> User:
    try:
        user = User.get(User.name == username)
    except:
        raise Unauthorized

    db_logger(action_id=LOGGING_LEVELS.LOGIN, done_by=user)
    return user

def signout(user_id: int):
    db_logger(logging_level=LOGGING_LEVELS.LOGOUT, done_by=user_id)

def new_message(user_id: int, **kwargs) -> int:
    try:
        message = Message.create(user=user_id, **kwargs)
    except:
        raise ActiveModelError

    db_logger(logging_level=LOGGING_LEVELS.MSG_NEW, done_by=user_id)
    return message.id

def all_messages(user_id: int, **kwargs):
    try:
        messages = Message.get(recipient=user_id, **kwargs).where(Message.status != 'DISABLED')
    except:
        raise ActiveModelError

    if not messages:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_ALL, done_by=user_id)
    return messages

def edit_message(user_id: int, pk: int, **kwargs):
    try:
        cn = Message.update(**kwargs).where(Message.sender == user_id and Message.id == pk)
    except:
        raise ActiveModelError

    if cn is None:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_EDIT, done_by=user_id)

def remove_message(user_id: int, pk: int):
    try:
        cn = Message.delete().where(Message.sender == user_id and Message.id == pk and Message.status != 'DELETED')
    except:
        raise ActiveModelError

    if cn is None:
        raise NoResourcesFound

    db_logger(logging_level=LOGGING_LEVELS.MSG_DEL, done_by=user_id)

def edit_user_display_name(pk: int, display_name: str):
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

    db_logger(logging_level=LOGGING_LEVELS.USER_EDIT_MAME, done_by=pk)

def edit_user_profile_picture(pk: int, data: bytes, extension: str):
    with open(f'{pk!r}-user-profile-picture.{extension!r}', 'rb') as fd:
        fd.write(data)
        fd.flush()
    db_logger(logging_level=LOGGING_LEVELS.USER_EDIT_PIC, done_by=pk)

def all_users(pk: int):
    try:
        users = User.select().where(User.id != pk)
        groups = (Group
                  .select()
                  .join(User)
                  .switch(Group)
                  .join(Joint)
                  .where(Group.created_by == pk or Joint.group == Group and Joint.user == pk))
    except:
        raise ActiveModelError

    db_logger(logging_level=LOGGING_LEVELS.USERS_ALL, done_by=pk)
    return users + list(groups)

def new_group(user_id: int, **kwargs):
    try:
        group = Group.create(created_by=user_id, **kwargs)
    except:
        raise ActiveModelError

    db_logger(logging_level=LOGGING_LEVELS.GROUP_NEW, done_by=user_id)
    return group.id

def new_member(user_id: int, pk: int, **kwargs):
    try:
        query = (Group
                 .select()
                 .join(User)
                 .switch(Group)
                 .join(Joint)
                 .where(Group.id == pk, Group.created_by == user_id or Joint.user == user_id and Joint.is_group_admin))
        results = list(query)
    except:
        raise ActiveModelError

    if not results:
        raise Unauthorized

    member = Joint.create(group=pk, **kwargs)
    db_logger(logging_level=LOGGING_LEVELS.MEMBER_ADD, done_by=user_id)
    return member.as_json()

def remove_member(user_id: int, member_id: int, group_id: int):
    try:
        if user_id == member_id:
            raise
        
        admin: Joint | None = Joint.get(Joint.user == user_id, Joint.group == group_id, Joint.is_group_admin)
        if admin is None:
            raise
        
        member: Joint | None = Joint.get(Joint.user == member_id, Joint.group == group_id)
        if member is None:
            raise
        member.delete_instance()
    except:
        raise ActiveModelError
    
    db_logger(logging_level=LOGGING_LEVELS.MEMBER_DEL, done_by=user_id)
    
def exit_group(member_id: int, group_id: int):
    try:
        member: Joint | None = Joint.get(Joint.user == member_id, Joint.group == group_id)
        if member is None or member.is_founder:
            raise
        member.delete_instance()
    except:
        raise ActiveModelError
    
    db_logger(logging_level=LOGGING_LEVELS.GROUP_EXIT, done_by=member_id)
    
def delete_group(user_id: int, group_id: int):
    try:
        group: Group | None = Group.get(Group.id == group_id, Group.created_by == user_id)
        if group is None:
            raise
        group.delete_instance()
    except:
        raise ActiveModelError
    
    db_logger(logging_level=LOGGING_LEVELS.GROUP_DEL, done_by=user_id)
