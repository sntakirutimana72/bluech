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
        await self.build_task(current_user=self.user_id, **self.request.params)

    async def _patch(self):
        """Edit an existing in service message"""
        msg_id = self.request.params.id
        MessageQueryManager.edit_message(self.user_id, msg_id, **self.request.body['message'])
        await self.build_task(resource_id=msg_id)

    async def _delete(self):
        """Delete a message by setting its status to `DISABLED|DELETED`"""
        current_user = self.user_id
        msg_id = self.request.params.id
        rec_id = MessageQueryManager.remove_message(current_user, msg_id)
        await self.build_task(resource_id=msg_id, from_=current_user, to_=rec_id)
