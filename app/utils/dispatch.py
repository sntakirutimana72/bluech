from .interfaces import Request
from ..urls import url_patterns

def dispatch(request: Request):
    full_path = request.ref_url.full_path

    for route in url_patterns[:-1]:
        if route.url == full_path:
            return route.controller
    return url_patterns[-1].controller
