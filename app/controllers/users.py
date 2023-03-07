import asyncio as io

from .base import Base
from ..utils.sql import UserQueryManager
from ..utils.layers import TasksLayer, PipeLayer

class Users(Base):
    async def _patch(self):
        """Edit user nickname"""
        pk = self.user_id
        UserQueryManager.edit_nickname(pk, self.request.body['user']['nickname'])
        await TasksLayer.build('edit_username_success', pk)

    async def _put(self, reader: io.StreamReader):
        """Change user profile picture"""
        pk = self.user_id
        options = {
            'user_id': pk,
            ''
        }
        await PipeLayer.download_avatar(reader, **self.request.body['user'])
        UserQueryManager.change_avatar(pk)
        await TasksLayer.build(self.request.protocol, pk)

    async def _get(self):
        """Fetch all current users and groups that you're associated to"""
        await TasksLayer.build(self.request.protocol, self.user_id)
