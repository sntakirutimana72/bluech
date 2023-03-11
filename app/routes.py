from .utils.router import router
from .controllers import *

route_patterns = [
    # session
    router(['signin', 'signout'], SessionController),
    # users
    router(['edit_username', 'change_user_avatar'], UsersController),
    # messages
    # router(['edit_'], MessagesController),
    # # groups
    # router('channels', ChannelsController),
]
