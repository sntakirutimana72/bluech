from .base import Base
from ..utils import sql
from ..utils.pipe import create_response_task

class Messages(Base):
    
    async def _post(self):
        """Create a new message"""
        message_id = sql.new_message(self.user_id, **self._request.body)
        await create_response_task(self._request.protocol, message_id)
        
    async def _get(self):
        """Fetch all messages that I'm part of"""
        await create_response_task(self._request.protocol, self.user_id)
