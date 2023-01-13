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

        create_task(self._in_service())

    async def _in_registry(self, user):
        self._is_servicing = None
        channel = Channel(self._writer, user)
        channels_q = channels_Q()

        await channels_q.push(channel)
        await pump(self._writer, Response.as_signin_success(user))
        await self._create_task('users', user.id)

    @staticmethod
    async def _create_task(proto, resource_id):
        tasks_q = tasks_Q()
        await tasks_q.push(AttributeDict({'protocol': proto, 'id': resource_id}))

    async def _in_submission(self, req):
        self._in_process(req)
        controller = dispatch(self._request)
        return await controller.exec()

    async def _in_service(self):
        try:
            req = await fetch(self._reader)
            resource = await self._in_submission(req)
            await self._in_registry(resource)
        except Exception as ex:
            await pump(self._writer, Response.as_exc(ex))

        self._request = None

    async def _in_transition(self, req):
        try:
            await self._in_submission(req)
        except Exception as ex:
            await pump(self._writer, Response.as_exc(ex))

        self._request = None

    async def _in_streaming(self):
        try:
            async for req in self._reader:
                await self._in_transition(req)
        except Exception as ex:
            print(ex)

    def _in_process(self, req):
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
