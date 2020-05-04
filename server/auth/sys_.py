import json
import asyncio
from socket import socket
from helpers.loggers import clilog, logging
from helpers.formatters import reader, writer


def acceptAuth_payload() -> bytes:
    acceptToken = json.dumps({'Accept-Auth': 'Access Granted!'})
    acceptToken = f'{len(acceptToken):04}' + acceptToken
    return acceptToken.encode('utf-8')


def verify(authToken: bytes) -> bool:
    authToken = json.loads(authToken.decode('utf-8'))
    return ('username' in authToken) and ('password' in authToken)


async def authenticate(conn: socket) -> tuple:
    try:
        await asyncio.sleep(.2)
        authToken = await reader(conn)

        if verify(authToken):
            await writer(conn, acceptAuth_payload())
            return conn, authToken
    except Exception as e:
        logging(e)
        clilog('Error occurred while authenticating client node::' + repr(e))
