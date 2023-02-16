from .base import Base
from ..utils import sql
from ..utils.layers import TasksLayer

class Channels(Base):

    async def _post(self):
        """Create a new channel"""
        channel_id = sql.new_channel(self.user_id, **self._request.body)
        await TasksLayer.build(self._request.protocol, channel_id)

    async def _put(self):
        """Add new member in the channel"""
        pk = self._request.params.id
        options = sql.new_member(self.user_id, pk, **self._request.body)
        await TasksLayer.build(self._request.protocol, None, **options)

    async def _pop(self):
        """Remove a channel member"""
        params = self._request.params
        sql.remove_member(self.user_id, **params)
        await TasksLayer.build(self._request.protocol, None, **params)

    async def _drop(self):
        """Exit channel"""
        params = {'member_id': self.user_id, 'channel_id': self._request.params.id}
        sql.exit_channel(**params)
        await TasksLayer.build(self._request.protocol, None, **params)

    async def _delete(self):
        """Delete a channel"""
        pk = self._request.params.id
        sql.delete_channel(self.user_id, pk)
        await TasksLayer.build(self._request.protocol, pk)