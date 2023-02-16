from typing import Any

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class RouteRef:

    def __init__(self, route_path: str):
        self.method, self.path = route_path.split(':', 1)

    @property
    def full_path(self):
        return f'{self.method!r}:{self.path!r}'

class Request:

    def __init__(self, req: dict[str, Any]):
        proto = req.pop('protocol')
        self.route_ref = RouteRef(proto)

        for name, value in req.items():
            setattr(self, name, value)

    @property
    def route_path(self) -> str:
        return self.route_ref.path

    @property
    def method(self) -> str:
        return self.route_ref.method

    @property
    def full_path(self) -> str:
        return self.route_ref.full_path
