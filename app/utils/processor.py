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

        io.create_task(self._in_stream())

    async def _in_registry(self, user):
        self._session = AttributeDict({'user_id': user.id, 'is_group': False})
        channel_layer = ChannelLayer(self._writer, user)

        await RepositoriesHub.channels_repository.push(channel_layer)
        await PipeLayer.pump(self._writer, Response.signin_success(user))
        await TasksLayer.build('users', user.id)

    def _in_submission(self, req):
        self._in_process(req)
        return dispatch(self._request).exec()

    async def _in_transition(self, req):
        try:
            result = await self._in_submission(req)
            if self._session is None:
                await self._in_registry(result)
        except CustomException as e:
            await PipeLayer.pump(self._writer, Response.signin_failure(**e.resp))
        except:
            await PipeLayer.pump(self._writer, Response.exception())
        self._request = None

    async def _in_stream(self):
        try:
            while True:
                req = await PipeLayer.fetch(self._reader)
                await self._in_transition(req)
        except:
            ...

    def _in_process(self, req):
        try:
            validated_req = AttributeDict(Validators.request(req))
            action_req = validated_req.pop('request')
            proto = validated_req.pop('protocol')

            if self._session is None:
                if proto != 'signin':
                    raise ProtocolValidationError
                req = Validators.signin(action_req)
            elif proto not in ALLOWED_ROUTES:
                raise ProtocolLookupError
            else:
                validator = getattr(Validators, proto)
                req = validator(action_req)

            validated_req |= req
            validated_req.session = self._session  # pass down the session context
            self._request = Request(ALLOWED_ROUTES[proto], validated_req)
        except sc.SchemaError:
            raise BadRequest
        except:
            raise CustomException
