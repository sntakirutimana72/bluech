from .base import Base
from ..utils import sql
from ..utils.pipe import create_response_task

class Groups(Base):

    async def _post(self):
        """Create a new group"""
        group_id = sql.new_group(self.user_id, **self._request.body)
        await create_response_task(self._request.protocol, group_id)

    async def _put(self):
        """Add new member in the group"""
        pk = self._request.params.id
        options = sql.new_member(self.user_id, pk, **self._request.body)
        await create_response_task(self._request.protocol, None, **options)

    async def _pop(self):
        """Remove a group member"""

    async def _drop(self):
        """Exit group"""

    async def _delete(self):
        """Delete a group"""
