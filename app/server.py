from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from .utils.parsers.env_vars import ServerArgumentParser

def serve(**kwargs):
    arg_parser = ServerArgumentParser(**kwargs) 
    
    address = arg_parser.address()
    
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    
    num_of_max_cons, is_async = arg_parser.limitations()
    
    server.listen(num_of_max_cons)
    server.setblocking(is_async)
