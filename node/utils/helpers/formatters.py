import json
import time
import asyncio
from socket import socket
from datetime import datetime
from utils.loggers.ilogger import logging


def payloader(json_like: dict) -> bytes:
    json_like.setdefault('time_', time.time())
    return jspayloader(json.dumps(json_like))


async def reader(node: socket) -> bytes:
    loop = asyncio.get_running_loop()
    load_size = await loop.sock_recv(node, 4)

    try:
        load_size = int(load_size)
        response = await loop.sock_recv(node, load_size)
    except Exception as e:
        logging(e)
        # cli('Error occurred while reading from node::' + repr(e))
    else:
        return response


def timesign(timestamp: str) -> str:
    timeSignature = datetime.fromtimestamp(timestamp)

    if timeSignature.date() != datetime.now().date():
        timeSignature = timeSignature.strftime('%a %b-%d-%Y %H:%M')
    else:
        timeSignature = 'Today ' + timeSignature.strftime('%H:%M')

    return timeSignature


async def writer(node: socket, load: bytes):
    await asyncio.get_running_loop().sock_sendall(node, load)


async def decompress(update: bytes) -> tuple:
    update = json.loads(update.decode('utf-8'))
    route = update.pop('route')

    if route == '/message':
        update['from_'] = f"@{update['from_']}".replace(';', '@')
        update['time_'] = timesign(update['time_'])

        if not update['to_']:
            update['to_'] = '@'
        else:
            update['to_'] = update['from_']

        return 'message', update

    if route in ['/update', '/users']:
        return 'user', update['msg_'].split(';')

    return None, None


def jspayloader(message: str) -> bytes:
    message = f'{len(message):04}' + message
    return message.encode('utf-8')
