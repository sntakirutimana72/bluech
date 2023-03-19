from .utils.router import router
from .controllers import *

route_patterns = [
    router(['signin', 'signout'], SessionController),
    router(['edit_username', 'change_user_avatar'], UsersController),
    router(['new_message', 'edit_message', 'remove_message', 'all_messages'], MessagesController),
]
