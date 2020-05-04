import asyncio
from helpers.servicer import servicing
from helpers.skt_connect import newServer
from helpers.loggers import clilog, logging
from helpers.broadcaster import broadcasting

__CONNECTED__ = {}
m_lock = asyncio.Lock()
c_lock = asyncio.Lock()
MESSAGES = asyncio.Queue()


async def run():
    try:
        logging('Attempting to start server..', 'i')
        clilog('Attempting to start server..', 'di-white')

        skt_server = newServer()

        if skt_server:
            skt_server, _ = skt_server
            logging('SERVER STARTED..', 'i')
            clilog(f' Server started at `{_[0]}:{_[1]}`..', 'di-white')
            clilog('Server Connection initiated successfully.!', 'green')
            clilog(' Waiting for new connections..', 'di-yellow')

            loop = asyncio.get_running_loop()
            loop.create_task(broadcasting(__CONNECTED__, MESSAGES, c_lock, m_lock))
            while True:
                conns = await loop.sock_accept(skt_server)
                loop.create_task(servicing(
                    conns, __CONNECTED__, MESSAGES, c_lock, m_lock
                ))
        else:
            logging('Failed to start server.')
    except Exception as e:
        logging(e)
        logging('Server terminated', 'i')


if __name__ == '__main__':
    asyncio.run(run())
