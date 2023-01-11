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
# :Messages
#
# :new_message validator
new_messge_validator = Schema({
    'body': {
        'recipient_id': int,
        'description': str,
        Optional('reply_to'): int
    }
})
# :edit_message validator
edit_messge_validator = Schema({
    'body': {
        'description': str
    },
    'params': {'message_id': int}
})
# :remove_message validator
remove_messge_validator = Schema({
    'params': {'message_id': int}
})
