import socket
from utils.auth import * 
from utils.loggers.ilogger import logging


def cliconnect(connect_address: tuple) -> socket.socket:
    try:
        client_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_node.connect(connect_address)
        client_node.setblocking(False)
        return client_node
    except Exception as e:
        logging(e)
