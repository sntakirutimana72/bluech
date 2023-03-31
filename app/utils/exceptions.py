__all__ = (
    'CustomException',
    'Unauthorized',
    'BadRequest',
    'ActiveRecordError',
    'ResourceNotChanged',
    'ResourceNotFound'
)

class CustomException(BaseException):
    code = 500
    message = 'Internal Error'
    proto = 'internal_error'

    def __init__(self, debug_msg=None):
        super().__init__(self.message)
        self.debug_message = debug_msg if debug_msg else self.message

    def __str__(self):
        return f'[{self.code}:{self.message}] ~ {self.debug_message}'

    @property
    def to_json(self):
        return {
            'status': self.code,
            'message': self.message,
            'proto': self.proto
        }

class Unauthorized(CustomException):
    code = 401
    message = 'Unauthorized'
    proto = 'signin_failure'

class BadRequest(CustomException):
    code = 400
    message = 'Bad Request'
    proto = 'invalid_request'

class ActiveRecordError(CustomException):
    code = 501
    message = 'Active Record operation failure'
    proto = 'active_record_error'

class ResourceNotFound(CustomException):
    code = 404
    message = 'Resource Not Found'
    proto = 'resource_not_found'

class ResourceNotChanged(CustomException):
    code = 304
    message = 'Resource was already up to date.'
    proto = 'resource_not_changed'
