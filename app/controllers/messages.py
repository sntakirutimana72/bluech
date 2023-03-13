from .base import Base
from ..utils.sql import MessageQueryManager

class Messages(Base):
    async def _post(self):
        """Create a new message"""
        message = self.request.body.pop('message')
        message['sender'] = self.user_id
        msg_id = MessageQueryManager.new_message(**message)
        await self.build_task(resource_id=msg_id)

    async def _get(self):
        """Fetch all messages that I'm part of"""
        await self.build_task(recipient=self.user_id)

    async def _patch(self):
        """Edit an existing in service message"""
        msg_id = self.request.params.message_id
        MessageQueryManager.edit_message(self.user_id, msg_id, **self.request.body)
        await self.build_task(resource_id=msg_id)

    async def _delete(self):
        """Delete a message by setting its status to `DISABLED|DELETED`"""
        msg_id = self.request.params.message_id
        MessageQueryManager.remove_message(self.user_id, msg_id)
        await self.build_task(message_id=msg_id, sender_id=self.user_id)
