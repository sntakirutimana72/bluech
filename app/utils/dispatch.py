from ..routes import route_patterns
from ..interfaces import Request

def dispatch(req: Request):
    for route in route_patterns:
        if route.url == req.full_path:
            return route.controller(req)
