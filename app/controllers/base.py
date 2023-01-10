from ..utils.interfaces import Request

class Base(object):
    def __init__(request: Request):
        self._request = request
