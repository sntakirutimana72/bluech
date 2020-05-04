import json
import asyncio
from socket import socket
from models.sys_ import new_inode
from helpers.fetcher import fetching


class iNode(object):

    def __init__(self, *largs):
        self._user = None
        self._fromaddr = None
        self._node = largs[0][0]
        self._configure(largs[0][1], *largs[1:])

    def _configure(self, *args):
        self._user = json.loads(args[0].decode('utf-8'))
        self._fromaddr = {'ip': args[1][0], 'port': args[1][1]}

    def fromaddr(self) -> str:
        return f"{self._fromaddr['ip']}:{self._fromaddr['port']}"

    def node(self) -> socket:
        return self._node

    def name(self) -> str:
        return self._user['username']


async def register(ssls: tuple, clocals: dict, mlocals: dict, clk, mlk):
    inode = iNode(*ssls)

    async with clk:
        all_ids = tuple(clocals.keys())
        clocals.setdefault(inode.name(), inode)

    loop = asyncio.get_running_loop()
    if all_ids:
        loop.create_task(new_inode(inode.name(), all_ids, mlocals, mlk))

    await asyncio.sleep(.5)
    loop.create_task(fetching(inode, mlocals, mlk))
