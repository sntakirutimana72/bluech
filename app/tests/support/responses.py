import schema as cma

class Skeletons:
    @staticmethod
    def required():
        return {
            'status': int,
            'proto': str
        }

    @classmethod
    def remove_message(cls, data):
        return cma.Schema({
            **cls.required(),
            'benefactor': {
                'id': int,
                'email': str,
                'nickname': str
            },
            'message_id': int
        }).is_valid(data)

    @classmethod
    def new_message(cls, data):
        return cma.Schema({
            **cls.required(),
            'message': {
                'id': int,
                'description': str,
                'is_edited': bool,
                'sender': {
                    'id': int,
                    'email': str,
                    'nickname': str
                },
                'sent_date': str,
                'last_update': cma.Or(str, None)
            }
        }).is_valid(data)
