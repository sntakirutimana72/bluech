from ..routes import route_patterns

def _handler(url, db, **options):
    Handler = None
    
    for route in route_patterns:
        if route.url == url:
            Handler = route.handler
            break
    
    if Handler is None:
        raise Exception('ControllerLookupError')
    
    return Handler(url, db, **options)
    