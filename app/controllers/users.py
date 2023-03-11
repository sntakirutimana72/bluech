from .base import Base
from ..utils.sql import UserQueryManager
from ..utils.layers import TasksLayer, PipeLayer
from ..utils.commons import filter_dict_items

class Users(Base):
    async def _patch(self):
        """Edit user nickname"""
        pk = self.user_id
        UserQueryManager.edit_nickname(pk, self.request.body['user']['nickname'])
        await TasksLayer.build('edit_username_success', pk)

    async def _put(self):
        """Change user profile picture"""
        pk = self.user_id
        only = ('content_length', 'content_type')
        options = {
            'user_id': pk,
            **filter_dict_items(self.request.__dict__, only=only)
        }
        await PipeLayer.download_avatar(self.request.processor.reader, **options)
        UserQueryManager.change_avatar(pk)
        await TasksLayer.build('change_user_avatar_success', pk)
