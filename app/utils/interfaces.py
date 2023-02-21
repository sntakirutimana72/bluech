from typing import Any

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class RouteRef:
    def __init__(self, route: str):
        self.full_path = route
        self.method, self.path = route.split(':', 1)

class Request:
    content_length: int
    """The size of the :param:~body content"""

    content_type: str
    """The type of the :param:~body content"""

    body: AttributeDict
    """Carries all essential data required to complement the request"""

    params: AttributeDict
    """Carries the secondary data that accommodate the essential data"""

    protocol: str
    """Unique service identifier/signature used to delegate the right consumers"""

    route_ref: RouteRef
    """Resolves the :attr:~protocol in order to determine the right consumers to dispatch"""

    session: AttributeDict
    """Holds the current connection metadata & authenticity"""

    def __init__(self, route: str, req: dict[str, Any]):
        self.route_ref = RouteRef(route)
        [setattr(self, *props) for props in req.items()]

    @property
    def route_path(self) -> str:
        return self.route_ref.path

    @property
    def method(self) -> str:
        return self.route_ref.method

    @property
    def full_path(self) -> str:
        return self.route_ref.full_path
