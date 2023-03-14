from .utils.router import router
from .controllers import *

route_patterns = [
    # session
    router(['signin', 'signout'], SessionController),
    # users
    router(['edit_username', 'change_user_avatar'], UsersController),
    # messages
    router(['new_message', 'edit_message'], MessagesController),
    # # groups
    # router('channels', ChannelsController),
]
