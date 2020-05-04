import asyncio
from helpers.loggers import clilog, logging
from helpers.formatters import recfilter, writer, payloader


async def broadcasting(clocals: dict, mlocals: asyncio.Queue, clk: asyncio.Lock, mlk: asyncio.Lock):
    while True:
        if not mlocals.empty():
            try:
                imessage = await mlocals.get()
                clilog(f'  ..route={imessage.route}, message={imessage.msg_}', 'di-white')

                if imessage.route != '/rename':
                    async with clk:
                        inodes = list(clocals.values())
                    for inode in recfilter(imessage.to_, imessage.from_, inodes):
                        await writer(inode, payloader(imessage.export()))
            except Exception as e:
                logging(e)
                clilog(repr(e))
        else:
            await asyncio.sleep(1)
