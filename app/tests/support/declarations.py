from ...settings import CONTENT_TYPES

class Models:
    @staticmethod
    def user(**others):
        return {'email': 'admin@test.eu', 'password': 'test@123', 'nickname': 'admin760', **others}

    @staticmethod
    def channel(**others):
        return {'nickname': 'channel_728', **others}

    @staticmethod
    def resource(**others):
        return {'location': 'app/ext_static/images/profile.png', **others}

    @staticmethod
    def activity(**others):
        return {'level': 1, **others}

    @staticmethod
    def activity_log(**others):
        return {'summary': ':admin logged in', **others}

class RequestSpecs:
    @staticmethod
    def head(proto: str, content_size=0, content_type=CONTENT_TYPES[0]):
        return {
            'content_length': content_size,
            'content_type': content_type,
            'protocol': proto
        }

    @classmethod
    def for_validators(cls, proto='signin', c_size=342, c_type=CONTENT_TYPES[0]):
        return {
            **cls.head(proto, c_size, c_type),
            'request': {
                'body': {
                    'email': 'user_test_email@bluech.eu',
                    'password': 'test@1234'
                }
            }
        }

    @classmethod
    def signin(cls, **user):
        return {
            **cls.head('signin'),
            'request': {'body': {'user': user}}
        }

    @classmethod
    def signout(cls):
        return {**cls.head('signout'), 'request': {}}

    @classmethod
    def edit_username(cls):
        return {
            **cls.head('edit_username'),
            'request': {'body': {'user': {'nickname': 'new nickname'}}}
        }

    @classmethod
    def change_user_avatar(cls):
        return {
            **cls.head('change_user_avatar'),
            'request': {}
        }

    @classmethod
    def new_message(cls, **kwargs):
        return {
            **cls.head('new_message'),
            'request': {'body': {'message': {'description': 'Hi, friend!', **kwargs}}}
        }

    @classmethod
    def edit_message(cls, params: dict[str, str | int], **kwargs):
        return {
            **cls.head('edit_message'),
            'request': {
                'body': {'message': kwargs},
                'params': params
            }
        }
