from .utils.router import router

route_patterns = [
    # session
    router('signin', '[<CONTROLLER>]'),
    router('signout', '[<CONTROLLER>]'),
    # messages
    router('all_messages', '[<CONTROLLER>]'),
    router('new_message', '[<CONTROLLER>]'),
    router('edit_message', '[<CONTROLLER>]'),
    router('remove_message', '[<CONTROLLER>]'),
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
    # not found zone
    router('not_found', '[<NOT_FOUND>]')
]