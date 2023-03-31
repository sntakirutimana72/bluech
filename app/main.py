import asyncio

from .utils.middlewares import accept_conn
from .utils.repositories import db_conn
from .settings import HOST_URL, HOST_PORT

async def main():
    db_conn()
    server = await asyncio.start_server(accept_conn, HOST_URL, HOST_PORT)

    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {address}')

    async with server:
        await server.serve_forever()
