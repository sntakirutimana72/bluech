from .interfaces import Request
from ..routes import route_patterns
from ..controllers import BaseController

def dispatch(req: Request) -> BaseController:
    def lookup(patterns=route_patterns) -> BaseController:
        for pattern in patterns:
            if type(pattern) is list:
                if controller_instance := lookup(pattern):
                    return controller_instance
            elif pattern.url == req.full_path:
                return pattern.controller(req)

    return lookup()
