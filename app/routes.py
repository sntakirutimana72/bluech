from .utils.router import router
from .controllers import *

route_patterns = [
    # session
    router('signin', SessionController),
    # messages
    # router('messages', MessagesController),
    # # users
    # router('users', UsersController),
    # # groups
    # router('channels', ChannelsController),
]
