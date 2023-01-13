from .interfaces import Request
from ..routes import route_patterns
from ..controllers import BaseController

def dispatch(req: Request) -> BaseController:
    for route in route_patterns:
        if route.url == req.full_path:
            return route.controller(req)
