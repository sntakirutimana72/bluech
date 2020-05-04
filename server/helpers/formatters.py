import json
import time
import asyncio
from typing import List
from socket import socket
from datetime import datetime
from helpers.loggers import clilog, logging


def imsg_display(imsg, iname: str):
    clilog(f'   ${iname} :wrote to: @{imsg.to_} ~ `{imsg.msg_}`', 'orange')


def timesign(timestamp: str) -> str:
    timeSignature = datetime.fromtimestamp(timestamp)

    if timeSignature.date() != datetime.now().date():
        timeSignature = timeSignature.strftime('%a %b-%d-%Y %H:%M')
    else:
        timeSignature = 'Today ' + timeSignature.strftime('%H:%M')

    return timeSignature


def jspayloader(message: str) -> bytes:
    message = f'{len(message):04}' + message
    return message.encode('utf-8')


def payloader(json_like: dict) -> bytes:
    return jspayloader(json.dumps(json_like))


async def reader(node: socket) -> bytes:
    loop = asyncio.get_running_loop()
    load_size = await loop.sock_recv(node, 4)

    try:
        load_size = int(load_size)
        response = await loop.sock_recv(node, load_size)
    except Exception as e:
        logging(e)
        clilog('Error occurred while reading from node::' + repr(e))
    else:
        return response


async def writer(node: socket, load: bytes):
    await asyncio.get_running_loop().sock_sendall(node, load)


def recfilter(ids: tuple, exc: str, all_inodes: list) -> List[socket]:
    if not ids:
        return [inode.node() for inode in all_inodes if inode.name() != exc]
    else:
        return [inode.node() for inode in all_inodes if inode.name() in ids]
