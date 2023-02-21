from .base import Base
from ..utils.sql import UserQueryManager
from ..utils.layers import TasksLayer

class Users(Base):
    async def _patch(self):
        """Edit user nickname"""
        pk = self.user_id
        UserQueryManager.edit_nickname(pk, self._request.body.user.nickname)
        await TasksLayer.build('nickname_edited', pk)

    async def _put(self):
        """Change user profile picture"""
        pk = self.user_id
        body = self._request.body
        UserQueryManager.edit_user_profile_picture(pk, body.data, body.extension)
        await TasksLayer.build(self._request.protocol, pk)

    async def _get(self):
        """Fetch all current users and groups that you're associated to"""
        await TasksLayer.build(self._request.protocol, self.user_id)
