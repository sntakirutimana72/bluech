from ..models import User, Group

class Channel(object):

    def __init__(self, writer, channel_id):
        self.channel_id = channel_id
        self.writer = writer

    @property
    def is_group(self):
        return self.writer is None

    @property
    def model(self):
        if self.writer:
            return User.get_by_id(self.channel_id)
        return Group.get_by_id(self.channel_id)
