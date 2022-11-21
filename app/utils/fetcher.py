import asyncio
from models.message import register
from helpers.formatters import reader
from helpers.loggers import clilog, logging


async def fetching(inode, mlocals: asyncio.Queue, mlk: asyncio.Lock):
    try:
        e_message = await reader(inode.node())
        if e_message:
            await register(inode.name(), e_message, mlocals, mlk)
    except Exception as e:
        logging(e)
        clilog(repr(e))

    loop = asyncio.get_running_loop()
    loop.call_later(1, loop.create_task, fetching(inode, mlocals, mlk))
