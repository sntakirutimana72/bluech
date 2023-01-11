from .interfaces import Request
from ..routes import route_patterns

def dispatch(request: Request):
    full_path = request.ref_url.full_path
    
    for route in route_patterns[:-1]:
        if route.url == full_path:
            return route.controller
    return route_patterns[-1].controller
    