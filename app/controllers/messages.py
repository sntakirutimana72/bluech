from .base import Base
from ..utils import sql
from ..utils.layers import TasksLayer

class Messages(Base):

    async def _post(self):
        """Create a new message"""
        message_id = sql.new_message(self.user_id, **self._request.body)
        await TasksLayer.build(self._request.protocol, message_id)

    async def _get(self):
        """Fetch all messages that I'm part of"""
        await TasksLayer.build(self._request.protocol, None, **{
            'recipient': self.user_id,
            'sender': self._request.sender
        })

    async def _patch(self):
        """Edit an existing in service message"""
        message_id = self._request.params.message_id
        sql.edit_message(self.user_id, message_id, **self._request.body)
        await TasksLayer.build(self._request.protocol, message_id)

    async def _delete(self):
        """Delete a message by setting its status to `DISABLED|DELETED`"""
        message_id = self._request.params.message_id
        sql.remove_message(self.user_id, message_id)
        await TasksLayer.build(self._request.protocol, None, **{
            'message_id': message_id,
            'sender_id': self.user_id
        })
