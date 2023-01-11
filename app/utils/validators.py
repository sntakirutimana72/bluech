from schema import Schema, Or

from ..settings import CONTENT_TYPES

def enum_type(*enums):
    def validate(initial):
        return initial in enums
    return validate

req_validator = Schema({
    'content_type': enum_validate(*CONTENT_TYPES),
    'content_length': int,
    'route': str,
    'body': Or(str, dict, list)
})
