from .base import Base
from ..utils import sql
from ..utils.layers import TasksLayer

class Users(Base):

    async def _patch(self):
        """Edit user display name"""
        pk = self.user_id
        sql.edit_user_display_name(pk, self._request.body.display_name)
        await TasksLayer.build(self._request.protocol, pk)

    async def _put(self):
        """Change user profile picture"""
        pk = self.user_id
        body = self._request.body
        sql.edit_user_profile_picture(pk, body.data, body.extension)
        await TasksLayer.build(self._request.protocol, pk)

    async def _get(self):
        """Fetch all current users and groups that you're associated to"""
        await TasksLayer.build(self._request.protocol, self.user_id)
