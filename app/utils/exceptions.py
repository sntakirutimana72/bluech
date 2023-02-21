__all__ = (
    'CustomException',
    'Unauthorized',
    'BadRequest',
    'DataTypingError',
    'ProtocolLookupError',
    'ProtocolValidationError',
    'ResourceNotChanged',
    'ActiveModelError',
    'NoResourcesFound'
)

class CustomException(BaseException):
    code = 500
    message = ''

    def __init__(self):
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} ~ {super().__str__()}'

    @property
    def resp(self):
        return {
            'status': self.code,
            'message': self.message
        }

class Unauthorized(CustomException):
    code = 401
    message = 'Unauthorized'

class BadRequest(CustomException):
    code = 400
    message = 'Bad Request'

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

class ResourceNotChanged(CustomException):
    code = 304
    message = 'Resource was already up to date.'
