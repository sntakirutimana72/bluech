import socket
from helpers.configurer import config
from helpers.loggers import clilog, logging


def newServer() -> socket.socket:
    try:
        configs = dict(config('server-configs'))
        skt_address = configs['ip'], int(configs['port'])
        skt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        skt_server.bind(skt_address)
        skt_server.listen(int(configs['limit']))
        skt_server.setblocking(bool(configs['blocking']))
        return skt_server, skt_address
    except Exception as e:
        logging(e)
        clilog(repr(e))
