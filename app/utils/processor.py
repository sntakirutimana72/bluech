from asyncio import StreamReader, StreamWriter, create_task

from .interfaces import AttributeDict, Request
from .shareables import channels_Q
from .channels import Channel
from .pipe import fetch, pump, create_response_task
from .response import Response
from .validators import Validators
from .exceptions import ProtocolLookupError, ProtocolValidationError, CustomException
from .dispatch import dispatch
from ..settings import ALLOWED_ROUTES

class Processor:

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self._session: AttributeDict | None = None
        self._request: Request | None = None

        create_task(self._in_stream())

    async def _in_registry(self, user):
        self._session = AttributeDict({'user_id': user.id, 'is_group': False})
        channel = Channel(self._writer, user)
        channels_q = channels_Q()

        await channels_q.push(channel)
        await pump(self._writer, Response.as_signin_success(user))
        await create_response_task('users', user.id)

    async def _in_submission(self, req):
        self._in_process(req)
        controller = dispatch(self._request)

        return await controller.exec()

    async def _in_transition(self, req):
        try:
            result = await self._in_submission(req)
            if self._session is None:
                await self._in_registry(result)
        except CustomException as ex:
            await pump(self._writer, Response.as_exc(ex))

        self._request = None

    async def _in_stream(self):
        try:
            while True:
                req = await fetch(self._reader)
                await self._in_transition(req)
        except Exception as ex:
            print(ex)

    def _in_process(self, req):
        validated_req = AttributeDict(Validators.request(req))
        action_req = validated_req.pop('request')

        if self._session is None:
            if validated_req.protocol != 'signin':
                raise ProtocolValidationError
            req = Validators.signin(action_req)
        elif validated_req.protocol not in ALLOWED_ROUTES:
            raise ProtocolLookupError
        else:
            validator = getattr(Validators, validated_req.protocol)
            req = validator(action_req)

        validated_req |= req
        validated_req.session = self._session  # pass down the session context
        self._request = Request(validated_req)
