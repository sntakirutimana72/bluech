from schema import Schema, Or, Optional

from ..settings import CONTENT_TYPES

def enum_type(*enums):
    def validate(initial):
        return initial in enums
    return validate

# :default validator
req_validator = Schema({
    'content_type': enum_validate(*CONTENT_TYPES),
    'content_length': int,
    'route': str,
    'request': {
        'body': Or(None, {str: object}),
        Optional('params'): {str: int}
    }
})
#
# :Session
#
# :signin validator
signin_validator = Schema({
    'body': {
        'name': str
    }
})
#
# :Users | :Groups
#
# :display_name validator and it applies on both group and user factions
display_validator = Schema({
    'body': {
        'display_name': str
    }
    'params': {'entity_id': int}
})
#
# :Users
#
# :all_users validator
edit_profile_pic_validator = Schema({
    'body': {
        'data': str
    }
    'params': {'user_id': int}
})
#
# :Groups
#
# :new_group validator
new_group_validator = Schema({
    'body': {
        'name': str,
        'created_by': int,
        'is_private': bool
    }
})
# :new_member validator
new_member_validator = Schema({
    'body': {
        'user_id': str,
        'is_group_admin': bool
    },
    'params': {'group_id': int}
})
# :new_member validator
remove_member_validator = Schema({
    'body': None,
    'params': {
        'group_id': int,
        'member_id': int
    }
})
# :exit_group & :remove_group validator
exit_or_remove_group_validator = Schema({
    'body': None,
    'params': {'group_id': int}
})
# :group_privilege validator
assign_group_privilege_validator = Schema({
    'body': {
        'is_group_admin': bool
    },
    'params': {
        'group_id': int,
        'member_id': int
    }
})
#
# :Messages
#
# :new_message validator
new_message_validator = Schema({
    'body': {
        'recipient_id': int,
        'description': str,
        Optional('reply_to'): int
    }
})
# :edit_message validator
edit_message_validator = Schema({
    'body': {
        'description': str
    },
    'params': {'message_id': int}
})
# :remove_message validator
remove_message_validator = Schema({
    'params': {'message_id': int}
})
