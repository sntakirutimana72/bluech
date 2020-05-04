import json
import asyncio
from socket import socket
from utils.loggers.ilogger import logging
from utils.helpers.formatters import reader, writer, payloader


async def accept_auth(node: socket) -> bool:
    accept_res = await reader(node)
    accept_res = json.loads(accept_res.decode('utf-8'))
    return accept_res['Accept-Auth'] == 'Access Granted!'


async def sign(node: socket, authToken: dict):
    await writer(node, payloader(authToken))


async def authenticate(node: socket, authToken: dict) -> bool:
    try:
        await sign(node, authToken)
        await asyncio.sleep(.5)
        isAccepted = await accept_auth(node)
        return isAccepted
    except Exception as e:
        logging(e)
