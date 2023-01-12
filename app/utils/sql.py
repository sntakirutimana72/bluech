from ..models import User

def signin(username):
    user = User.get_or_none(User.name == username)
    return user.id if user else None

def signout():
    ...

def change_user_display_name(username, display_name):
    user = User.get_or_none(User.name == username)
    if user is None:
        return
    if user.display_name == display_name or User.get_or_none(User.display_name == display_name):
        return
    user.display_name = display_name
    user.save()

    return user.id
