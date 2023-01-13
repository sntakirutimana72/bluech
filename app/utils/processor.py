from asyncio import StreamReader, StreamWriter, create_task

from .interfaces import AttributeDict, Request
from .shareables import channels_Q, tasks_Q
from .channels import Channel
from .pipe import fetch, pump
from .response import Response
from .validators import Validators
from .exceptions import ProtocolLookupError, ProtocolValidationError
from .dispatch import dispatch
from ..settings import ALLOWED_ROUTES

class Processor:

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self._is_servicing = True
        self._request = None

        create_task(self._service_new())

    async def _register_new(self, user):
        self._is_servicing = None
        # Update Channels Queue
        channel = Channel(self._writer, user)
        channels_q = channels_Q()
        await channels_q.push(channel)
        # Ping back the channel
        await pump(self._writer, Response.as_signin_success(user))
        # Cache broadcast task in the corresponding queue
        await self._create_task('users', user.id)

    @staticmethod
    async def _create_task(proto, entity_id):
        tasks_q = tasks_Q()
        await tasks_q.push(AttributeDict({'protocol': proto, 'id': entity_id}))

    async def _service_new(self):
        # new connection is still in transit and haven't been cleared to operate
        try:
            req = await fetch(self._reader)
            self._process_request(req)
            # Invoke resource controller to handle the rest
            controller = dispatch(self._request)
            user = await controller.exec()
            await self._register_new(user)
        except Exception as ex:
            await pump(self._writer, Response.as_exc(ex))
        finally:
            self._request = None

    def _process_request(self, req):
        validated_req = AttributeDict(Validators.request(req))
        action_req = validated_req.pop('request')

        if self._is_servicing:
            if validated_req.protocol != 'signin':
                raise ProtocolValidationError
            req = Validators.signin(action_req)
        elif validated_req.protocol not in ALLOWED_ROUTES:
            raise ProtocolLookupError
        else:
            validator = getattr(Validators, validated_req.protocol)
            req = validator(action_req)

        validated_req |= req
        self._request = Request(validated_req)
