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
    def __init__(self, reader: io.StreamReader, writer: io.StreamWriter):
        self._reader = reader
        self._writer = writer
        self._session: AttributeDict | None = None
        self._request: Request | None = None

        io.create_task(self.gather())

    async def subscribe(self, user):
        user_id = user.id
        self._session = AttributeDict({'user_id': user_id, 'is_group': False})
        channel_layer = ChannelLayer(self._writer, user_id)

        await RepositoriesHub.channels_repository.push(channel_layer)
        await PipeLayer.pump(self._writer, Response.signin_success(user))
        await TasksLayer.build('users', user_id)
        
    async def unsubscribe(self):
        user_id = self._session.user_id
        self._session = None
        
        await RepositoriesHub.channels_repository.remove(user_id)
        await PipeLayer.pump(self._writer, Response.signout_success())
        await TasksLayer.build('remove_user', user_id)

    def resolve(self, request):
        self.sanitize(request)
        return dispatch(self._request).exec()

    async def process(self, request):
        try:
            result = await self.resolve(request)
            if self._session is None:
                await self.subscribe(result)
            elif self._request.protocol == 'signout':
                await self.unsubscribe()
        except CustomException as e:
            await PipeLayer.pump(self._writer, Response.signin_failure(**e.resp))
        except:
            await PipeLayer.pump(self._writer, Response.exception())
        self._request = None

    async def gather(self):
        try:
            while True:
                request = await PipeLayer.fetch(self._reader)
                await self.process(request)
        except:
            ...

    def sanitize(self, request):
        try:
            validated_req = AttributeDict(Validators.request(request))
            action_req = validated_req.pop('request')
            proto = validated_req.pop('protocol')

            if self._session is None:
                if proto != 'signin':
                    raise ProtocolValidationError
                request = Validators.signin(action_req)
            elif proto not in ALLOWED_ROUTES:
                raise ProtocolLookupError
            else:
                validator = getattr(Validators, proto)
                request = validator(action_req)

            validated_req |= request
            validated_req.session = self._session  # pass down the session context
            self._request = Request(ALLOWED_ROUTES[proto], validated_req)
        except sc.SchemaError:
            raise BadRequest
        except:
            raise CustomException
