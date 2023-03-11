import asyncio as io
import schema as sc
import traceback as tc

from .interfaces import AttributeDict, Request
from .repositories import RepositoriesHub
from .layers import ChannelLayer, Response, PipeLayer, TasksLayer
from .validators import Validators
from .exceptions import *
from .dispatch import dispatch
from ..settings import ALLOWED_ROUTES

# noinspection PyBroadException
class Processor:
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

    def resolve(self, raw_req):
        self.sanitize(raw_req)
        handler = dispatch(self.request).exec()
        return handler()

    async def process(self, raw_req):
        try:
            result = await self.resolve(raw_req)
            if self.session is None:
                await self.subscribe(result)
            elif self.request.protocol == 'signout':
                await self.unsubscribe()
        except CustomException as e:
            await PipeLayer.pump(self.writer, Response.make(**e.to_json))
        except:
            print(tc.print_exc())
            await PipeLayer.pump(self.writer, Response.internal_error())
        self.request = None

    async def gather(self):
        try:
            while True:
                raw_req = await PipeLayer.fetch(self.reader)
                await self.process(raw_req)
        except:
            ...

    def sanitize(self, raw_req):
        try:
            validated_req = AttributeDict(Validators.request(raw_req))
            action_req = validated_req.pop('request')
            proto = validated_req['protocol']
            request_after = {}

            if (proto not in ALLOWED_ROUTES) or (not self.session and proto != 'signin'):
                raise BadRequest
            elif hasattr(Validators, proto):
                request_after = getattr(Validators, proto)(action_req)

            validated_req |= request_after
            validated_req.processor = self
            validated_req.session = self.session  # pass down the session context
            self.request = Request(ALLOWED_ROUTES[proto], validated_req)
        except sc.SchemaError:
            raise BadRequest
        except:
            raise CustomException
