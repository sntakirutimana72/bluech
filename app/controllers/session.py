from .base import Base
from ..utils.interfaces import AttributeDict
from ..utils.layers import ChannelLayer, PipeLayer, Response
from ..utils.repositories import RepositoriesHub as Hub
from ..utils.sql import SessionQueryManager

class Session(Base):
    async def _post(self):
        proc = self.processor
        user = SessionQueryManager.signin(**self.request.body.user)
        ssid = user.id
        proc.session = AttributeDict({'user_id': ssid})
        channel_layer = ChannelLayer(proc.writer, ssid)
        participants_ids = Hub.channels_repository.keys

        await Hub.channels_repository.push(channel_layer)
        await PipeLayer.pump(proc.writer, Response.signin_success(user))
        await self.build_task(resource_id=ssid, ids=participants_ids)

    async def _delete(self):
        ssid = self.user_id
        proc = self.processor
        proc.session = None

        SessionQueryManager.signout(ssid)
        await Hub.channels_repository.remove(ssid)
        await PipeLayer.pump(proc.writer, Response.signout_success())
        await self.build_task(ssid=ssid, ids=Hub.channels_repository.keys)
