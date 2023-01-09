import asyncio

from .middlewares import service_connection
from .db_connect import db_connector
from .settings import HOST_URL, HOST_PORT
    

async def main():
    conn = db_connector()
    server = await asyncio.start_server(service_connection(db), HOST_URL, HOST_PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
