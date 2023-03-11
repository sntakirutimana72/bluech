from .base import Base
from ..utils.sql import MessageQueryManager
from ..utils.layers import TasksLayer

class Messages(Base):
    async def _post(self):
        """Create a new message"""
        message_id = MessageQueryManager.new_message(self.user_id, **self.request.body)
        await TasksLayer.build(self.request.protocol, message_id)

    async def _get(self):
        """Fetch all messages that I'm part of"""
        await TasksLayer.build(self.request.protocol, None, recipient=self.user_id)

    async def _patch(self):
        """Edit an existing in service message"""
        message_id = self.request.params.message_id
        MessageQueryManager.edit_message(self.user_id, message_id, **self.request.body)
        await TasksLayer.build(self.request.protocol, message_id)

    async def _delete(self):
        """Delete a message by setting its status to `DISABLED|DELETED`"""
        message_id = self.request.params.message_id
        MessageQueryManager.remove_message(self.user_id, message_id)
        await TasksLayer.build(self.request.protocol, None, **{
            'message_id': message_id,
            'sender_id': self.user_id
        })
