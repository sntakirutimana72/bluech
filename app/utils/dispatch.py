<<<<<<< HEAD
from .interfaces import Request
from ..routes import route_patterns

def dispatch(request: Request):
    full_path = request.ref_url.full_path
    
    for route in route_patterns[:-1]:
        if route.url == full_path:
            return route.controller
    return route_patterns[-1].controller
    
=======
from .interfaces import Request
from ..urls import url_patterns

def dispatch(request: Request):
    full_path = request.ref_url.full_path

    for route in url_patterns[:-1]:
        if route.url == full_path:
            return route.controller
    return url_patterns[-1].controller
>>>>>>> 160d46f1726a7832d7dbc02bbc7c5fc76667dfe5
