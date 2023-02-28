import asyncio as io
import schema as sc

from .interfaces import AttributeDict, Request
from .repositories import RepositoriesHub
from .layers import ChannelLayer, Response, PipeLayer, TasksLayer
from .validators import Validators
from .exceptions import *
from .dispatch import dispatch
from ..settings import ALLOWED_ROUTES

# noinspection PyBroadException
class Processor:
    proto: str | None

    def __init__(self, reader: io.StreamReader, writer: io.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.session: AttributeDict | None = None
        self.request: Request | None = None

        io.create_task(self.gather())

    async def subscribe(self, user):
        user_id = user.id
        self.session = AttributeDict({'user_id': user_id, 'is_group': False})
        channel_layer = ChannelLayer(self.writer, user_id)
        await RepositoriesHub.channels_repository.push(channel_layer)
        await PipeLayer.pump(self.writer, Response.signin_success(user))
        await TasksLayer.build('connected', user_id)

    async def unsubscribe(self):
        user_id = self.session.user_id
        self.session = None
        await RepositoriesHub.channels_repository.remove(user_id)
        await PipeLayer.pump(self.writer, Response.signout_success())
        await TasksLayer.build('disconnected', user_id)

    def resolve(self, request):
        self.sanitize(request)
        handler = dispatch(self.request).exec()
        if self.proto == 'change_user_avatar':
            return handler(self.reader)
        return handler()

    async def process(self, request):
        try:
            result = await self.resolve(request)
            if self.session is None:
                await self.subscribe(result)
            elif self.proto == 'signout':
                await self.unsubscribe()
        except CustomException as e:
            await PipeLayer.pump(self.writer, Response.make(**e.to_json))
        except:
            await PipeLayer.pump(self.writer, Response.internal_error())
        self.proto = None
        self.request = None

    async def gather(self):
        try:
            while True:
                request = await PipeLayer.fetch(self.reader)
                await self.process(request)
        except:
            ...

    def sanitize(self, request):
        try:
            validated_req = AttributeDict(Validators.request(request))
            action_req = validated_req.pop('request')
            self.proto = validated_req.pop('protocol')

            if (self.proto not in ALLOWED_ROUTES) or (not self.session and self.proto != 'signin'):
                raise BadRequest
            elif self.proto == 'signout':
                request = {}
            else:
                validator = getattr(Validators, self.proto)
                request = validator(action_req)

            validated_req |= request
            validated_req.session = self.session  # pass down the session context
            self.request = Request(ALLOWED_ROUTES[self.proto], validated_req)
        except sc.SchemaError:
            raise BadRequest
        except:
            raise CustomException
