from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from .configs.server import Config

def serve(**kwargs):
    address = Config.address(kwargs)
    
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    
    num_of_max_cons, is_async = Config.limitations(kwargs)
    
    server.listen(num_of_max_cons)
    server.setblocking(is_async)
