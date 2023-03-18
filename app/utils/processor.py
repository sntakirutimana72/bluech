import asyncio as io
import schema as sc
import traceback as tc

from .interfaces import AttributeDict, Request
from .layers import Response, PipeLayer
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

    def resolve(self, raw_req):
        self.sanitize(raw_req)
        handler = dispatch(self.request, self).exec()
        return handler()

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
            self.request = Request(ALLOWED_ROUTES[proto], validated_req)
        except sc.SchemaError:
            raise BadRequest
        except:
            raise CustomException

    async def process(self, raw_req):
        try:
            await self.resolve(raw_req)
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
