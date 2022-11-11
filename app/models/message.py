import json
import asyncio
from helpers.formatters import imsg_display


class iMessage(object):
    __routes__ = (
        '/users',  # broadcast users
        '/update',  # new user update
        '/rename',  # used to rename user
        '/message',  # send message to all
        '/message?group',  # send message to a specific group
        '/message?user',  # send message to a single direct user
    )

    def __init__(self, *largs):
        self.to_ = None
        self.msg_ = None
        self.time_ = None
        self.route = None
        self.from_ = largs[0]
        self._process(largs[1])

    def export(self):
        return {
            'time_': self.time_,
            'route': self.route,
            'from_': self.from_,
            'msg_': self.msg_,
            'to_': self.to_
        }

    def _process(self, message: bytes):
        jsonLikeMsg = json.loads(message.decode('utf-8'))
        route = jsonLikeMsg['route']

        if route not in self.__routes__:
            raise Exception(f'`{route}`::Unknown protocol')

        self.time_ = jsonLikeMsg['time_']
        self.to_ = jsonLikeMsg['to_']
        self.msg_ = jsonLikeMsg['msg_']
        self.route = route


async def register(iname: str, msg: bytes, mlocals: asyncio.Queue, mlk: asyncio.Lock):
    imessage = iMessage(iname, msg)
    imsg_display(imessage, iname)

    async with mlk:
        await mlocals.put(imessage)
