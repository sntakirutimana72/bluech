from socket import socket


def close(node: socket, isserved: bool = False):
    node.close()
