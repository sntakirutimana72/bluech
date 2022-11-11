import json
import asyncio
from time import time
from models.message import register


async def new_inode(inew: str, ids: tuple, mlocals: asyncio.Queue, mlk: asyncio.Lock):
    update_to_others = json.dumps({
        'to_': ids, 'msg_': inew, 'from_': '',
        'time_': time(), 'route': '/update'
    }).encode('utf-8')

    update_to_new = json.dumps({
        'msg_': ';'.join(ids), 'to_': (inew, ),
        'time_': time(), 'route': '/users', 'from_': ''
    }).encode('utf-8')

    loop = asyncio.get_running_loop()
    loop.create_task(register('', update_to_others, mlocals, mlk))
    loop.create_task(register('', update_to_new, mlocals, mlk))
