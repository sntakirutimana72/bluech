from .base import Base
from ..utils.sql import UserQueryManager
from ..utils.layers import PipeLayer
from ..utils.commons import filter_dict_items

class Users(Base):
    async def _patch(self):
        """Edit user nickname"""
        current_user = self.user_id
        UserQueryManager.edit_nickname(current_user, self.request.body['user']['nickname'])
        await self.build_task(resource_id=current_user)

    async def _put(self):
        """Change user profile picture"""
        current_user = self.user_id
        only = ('content_length', 'content_type')
        options = {
            'current_user': current_user,
            **filter_dict_items(self.request.__dict__, only=only)
        }
        await PipeLayer.download_avatar(self.processor.reader, **options)
        UserQueryManager.change_avatar(current_user)
        await self.build_task(resource_id=current_user)
