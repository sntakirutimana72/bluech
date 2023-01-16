class CustomException(Exception):
    code = 500
    message = ''

    def __init__(self):
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code!r}~{super().__str__()!r}'

class Unauthorized(CustomException):
    code = 401
    message = 'Unauthorized'

class DataTypingError(CustomException):
    message = 'Must be one of `json` | `text`'

class ProtocolValidationError(CustomException):
    code = 403

class ProtocolLookupError(CustomException):
    code = 404
    
class ActiveModelError(CustomException):
    code = 501
    message = 'DB Model operation failure'
    
class NoResourcesFound(CustomException):
    code = 404
    message = 'Not Found'
