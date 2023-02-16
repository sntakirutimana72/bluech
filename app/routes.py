from .utils.router import router
from .controllers import *

route_patterns = [
    # session
    router(('signin', 'signout',), SessionController),
    # messages
    router(
        ('new_message', 'all_messages', 'edit_message', 'remove_message',),
        MessagesController
    ),
    # users
    router(
        ('edit_username', 'edit_profile_pic', 'all_users',),
        UsersController
    ),
    # groups
    router(
        ('new_group', 'new_member', 'remove_member', 'exit_group', 'remove_group', 'assign_group_privilege',),
        ChannelsController
    ),
]
