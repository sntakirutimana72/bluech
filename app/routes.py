from .utils.router import router
from .controllers import SessionController
from .controllers import MessagesController

route_patterns = [
    # session
    router(('signin', 'signout',), SessionController),
    # messages
    router(
        ('new_message', 'all_messages', 'edit_message', 'remove_message',),
        MessagesController
    ),
    # users
    router('edit_username', '[<CONTROLLER>]'),     # (edit display name)
    router('edit_profile_pic', '[<CONTROLLER>]'),  # (change profile picture)
    router('all_users', '[<CONTROLLER>]'),         # (fetch all users)
    # groups
    router('new_group', '[<CONTROLLER>]'),         # (create group)
    router('new_member', '[<CONTROLLER>]'),        # (add member)
    router('remove_member', '[<CONTROLLER>]'),     # (remove member)
    router('exit_group', '[<CONTROLLER>]'),        # (leave group)
    router('remove_group', '[<CONTROLLER>]'),      # (delete group)
    router('group_privilege', '[<CONTROLLER>]'),   # (assign privilege)
]
