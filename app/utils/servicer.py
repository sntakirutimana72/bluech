import asyncio
from auth import sys_
from models.node import register
from helpers.terminator import close
from helpers.loggers import clilog, logging


async def servicing(conns: tuple, clocals: dict, mlocals: asyncio.Queue, clk: asyncio.Lock, mlk: asyncio.Lock):
    ssl_node = await sys_.authenticate(conns[0])

    if ssl_node:
        try:
            clilog(f' ..New node joined ~ @{conns[1][0]}:{conns[1][1]}', 'gray')
            await asyncio.sleep(.02)
            await register((ssl_node, conns[1]), clocals, mlocals, clk, mlk)
        except Exception as e:
            logging(e)
            clilog('Error occurred while servicing new connection::' + repr(e))
    else:
        close(conns[0])
